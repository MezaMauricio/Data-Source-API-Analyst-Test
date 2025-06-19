# Error and Rate Handling

This file documents the strategies used to handle GitHub API quota limits, request errors, and retry logic — implemented in both Python and Postman.

---

## 1 · Quota Limits (Rate Limits)

| Token Type               | Window | Limit         | Control Endpoint              |
|--------------------------|--------|---------------|-------------------------------|
| **No token**             | 1 hr   | 60 requests   | `/rate_limit`                 |
| **Classic PAT**          | 1 hr   | 5,000 requests| `/rate_limit`                 |
| **Search** (`/search/*`) | 1 min  | 30 requests   | Headers: `X-RateLimit-Search-*` |

```json
GET /rate_limit → 200 OK
{
  "rate":   { "limit": 5000, "remaining": 4975, "reset": 1718649600 },
  "search": { "limit": 30,   "remaining": 28,   "reset": 1718649330 }
}
```

> The `reset` field is a UTC Epoch timestamp. Use `reset - time.time()` to calculate remaining seconds.

### Python Control Strategy

```python
import time, requests

def safe_get(url, **kwargs):
    while True:
        r = requests.get(url, **kwargs)
        if r.status_code == 403 and r.headers.get("X-RateLimit-Remaining") == "0":
            wait = int(r.headers["X-RateLimit-Reset"]) - time.time()
            print(f"[RateLimit] reached, waiting {wait:.0f}s…")
            time.sleep(max(wait, 0) + 1)
            continue
        r.raise_for_status()
        return r
```

### Postman Pre-request Script (JS)

```javascript
if (pm.response.code === 403 && pm.response.headers.get("X-RateLimit-Remaining") === "0") {
  const reset = pm.response.headers.get("X-RateLimit-Reset");
  const wait  = reset - Math.floor(Date.now() / 1000);
  console.log(`Rate limit hit, waiting ${wait}s`);
  setTimeout(() => pm.sendRequest(pm.request), (wait + 1) * 1000);
}
```

---

## 2 · Common Error Types

| Code                     | Common Cause                                           | Diagnosis                        | Recommended Solution                                |
|--------------------------|--------------------------------------------------------|----------------------------------|-----------------------------------------------------|
| **401 Unauthorized**     | Token is invalid, expired, or lacks required scopes    | Check `WWW-Authenticate` header | Regenerate PAT and ensure `public_repo` scope       |
| **403 Forbidden** (rate) | Rate limit exceeded                                    | Check `X-RateLimit-*` headers    | Wait until `reset` and retry                        |
| **403 Forbidden** (abuse)| Too many parallel requests                             | Look for `Retry-After` header    | Reduce concurrency, apply retry delay               |
| **422 Validation Failed**| Malformed or out-of-range parameters (e.g., `per_page`) | JSON response contains `errors` | Fix request payload or parameter values             |
| **404 Not Found**        | Path or repo does not exist or is private              | –                                | Verify repo `owner/name` and permissions            |

---

## 3 · Retry Strategy

- **GET Requests:** Retry up to 3 times with exponential back-off (1s, 2s, 4s…)
- **5xx Errors:** Wait 10 seconds and retry
- **4xx Errors:** Only retry for 403 (*rate-limit*) or 409/422 if payload is fixable

---

## 4 · Best Practices

- Cache static responses (e.g., repo metadata) to reduce API usage
- Use `per_page=100` to minimize pagination calls
- Serialize checkpoint progress to resume after interruption
- Log `X-RateLimit-Remaining` to monitor usage and debug

---

*Updated: 18 Jun 2025*
