# API Reference — GitHub REST v3

> Tested version: **2022-11-28** – All requests use the header `X-GitHub-Api-Version: 2022-11-28`.

## Table of Implemented Endpoints

| Nº | Resource | Method | Path | Key Parameters | Pagination | Notes |
|----|----------|--------|------|----------------|------------|-------|
| 1 | **Search Repositories** | `GET` | `/search/repositories` | `q` (query), `sort`, `order`, `per_page`, `page` | Yes (`Link`) | *Search* results have an additional limit of **30 req/min**. |
| 2 | **Repository Commits** | `GET` | `/repos/{owner}/{repo}/commits` | `sha`, `since`, `until`, `path`, `author`, `per_page`, `page` | Yes | GPG signatures, stats, etc. require extra scopes (`repo`). |
| 3 | **File / Folder Contents** | `GET` | `/repos/{owner}/{repo}/contents/{path}` | `ref` (branch / tag / SHA) | No (returns full list if folder) | Returns an array for folders; returns an object with Base64 `content` for files. |
| 4 | **Rate Limit** | `GET` | `/rate_limit` | — | — | Useful for monitoring usage.

---

## Authentication

```http
Authorization: Bearer <PERSONAL_ACCESS_TOKEN>
X-GitHub-Api-Version: 2022-11-28
Accept: application/vnd.github+json
```

> **Minimum scopes:** `public_repo` is sufficient for public endpoints; add `repo` if you need access to private repos or detailed commit data.

---

## Request and Response Examples

### 1· Repository Search

**Request**
```bash
GET https://api.github.com/search/repositories?q=language:python+stars:>50000&per_page=5
```

**200 OK (truncated body)**
```json
{
  "total_count": 1204,
  "incomplete_results": false,
  "items": [
    {
      "id": 4164482,
      "name": "django",
      "full_name": "django/django",
      "owner": { "login": "django" },
      "html_url": "https://github.com/django/django",
      "stargazers_count": 75700,
      "language": "Python",
      "license": { "spdx_id": "BSD-3-Clause" },
      "updated_at": "2025-06-15T18:10:27Z"
    }
  ]
}
```

### 2· Commits

```bash
GET https://api.github.com/repos/pandas-dev/pandas/commits?sha=main&since=2025-05-01T00:00:00Z&per_page=100
```

Response (first item):
```json
{
  "sha": "6f5c1c8…",
  "commit": {
    "author": {
      "name": "Jeff Reback",
      "email": "jeff@pandas.io",
      "date": "2025-06-12T11:42:57Z"
    },
    "message": "BUG: fix groupby edge case",
    "tree": { "sha": "adf4…" },
    "comment_count": 0
  },
  "author": { "login": "jreback" },
  "files": [ … ]
}
```

### 3· File Content

```bash
GET https://api.github.com/repos/tensorflow/tensorflow/contents/README.md?ref=main
```

```json
{
  "name": "README.md",
  "path": "README.md",
  "sha": "0f9e…",
  "size": 3621,
  "encoding": "base64",
  "content": "IyBUZW5zb3JmbG93…==",
  "html_url": "https://github.com/tensorflow/tensorflow/blob/main/README.md"
}
```

---

## Common Parameters

| Param | Description | Example |
|-------|-------------|---------|
| `per_page` | Number of items per page (1–100) | `per_page=100` |
| `page` | Page index (starts at 1) | `page=3` |
| `since` / `until` | Filter *commits* by ISO-8601 date | `since=2025-01-01T00:00:00Z` |
| `ref` | Branch, tag, or SHA for Contents | `ref=develop` |

---

## Pagination Headers

```
Link: <https://api.github.com/…&page=2>; rel="next", <…&page=5>; rel="last"
```

In code, parse the `rel="next"` link; if it exists, continue iterating.

---

## Quick `curl` Call (automatic pagination with jq)

```bash
curl -H "Authorization: Bearer $TOKEN" \
     -H "X-GitHub-Api-Version: 2022-11-28" \
     "https://api.github.com/repos/pandas-dev/pandas/commits?per_page=100" \
| jq -r '.[].sha'
```

---

> For additional details, see the official API documentation: <https://docs.github.com/en/rest>.
