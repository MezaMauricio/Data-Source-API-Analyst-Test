"""
Auth & Helpers — simple GitHub API module
=========================================

This module includes:
---------------------
1. `build_headers()`   → sets up headers with your token and API version
2. `paginated_get()`   → handles pagination and rate limits
3. `GitHubClient`      → a quick way to run API calls, like:
                         `for repo in client.get('/search/repositories', q='python'):`


"""
from __future__ import annotations

import os
import time
from typing import Dict, Iterator, Any, Optional

import requests

BASE_URL: str = "https://api.github.com"
LATEST_API_VERSION: str = "2022-11-28"
USER_AGENT: str = "data-source-api-analyst-homework/0.1"


def build_headers(token: str | None = None,
                  api_version: str = LATEST_API_VERSION) -> Dict[str, str]:
    """Return **immutable** headers for GitHub REST v3 calls."""
    token = token or os.getenv("GITHUB_PAT")
    if not token:
        raise RuntimeError(
            "GitHub token not found — set env var GITHUB_PAT or pass token='…'")
    return {
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": api_version,
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
    }


def paginated_get(url: str,
                  params: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None,
                  session: Optional[requests.Session] = None) -> Iterator[Dict[str, Any]]:
    """Yield items (dict) across pages. Auto‑sleeps on 403 *rate limit* responses."""
    sess = session or requests.Session()
    next_url = url
    while next_url:
        resp = sess.get(next_url, params=params, headers=headers, timeout=30)

        # --- Rate‑limit handling ------------------------------------------------
        if resp.status_code == 403 and resp.headers.get("X-RateLimit-Remaining") == "0":
            reset = int(resp.headers["X-RateLimit-Reset"])
            wait = max(reset - int(time.time()), 0) + 1
            print(f"[RateLimit] exhausted → sleeping {wait}s …")
            time.sleep(wait)
            continue  # retry the same URL

        resp.raise_for_status()
        data = resp.json()
        # /search/* endpoints wrap results under "items"
        if isinstance(data, dict) and "items" in data:
            yield from data["items"]
        else:
            yield from data if isinstance(data, list) else [data]

        # Parse pagination
        next_url = resp.links.get("next", {}).get("url")
        params = None  # subsequent pages have params embedded


class GitHubClient:
    """Lightweight wrapper simplifying calls inside the notebook."""

    def __init__(self, token: str | None = None):
        self.headers = build_headers(token)
        self.session = requests.Session()

    def get(self, endpoint: str, **params) -> Iterator[Dict[str, Any]]:
        url = endpoint if endpoint.startswith("http") else f"{BASE_URL}{endpoint}"
        return paginated_get(url, params=params or None, headers=self.headers, session=self.session)

    # Convenience helpers (optional)
    def search_repositories(self, q: str, **params):
        return self.get("/search/repositories", q=q, **params)

    def commits(self, owner: str, repo: str, **params):
        return self.get(f"/repos/{owner}/{repo}/commits", **params)

    def contents(self, owner: str, repo: str, path: str = "", **params):
        return self.get(f"/repos/{owner}/{repo}/contents/{path}", **params)


# ---------------------------------------------------------------------
# Quick test (only runs if you execute this file directly)
# Example:
#     $ python content/auth_and_helpers.py /rate_limit
# ---------------------------------------------------------------------
if __name__ == "__main__":
    import argparse, json

    argp = argparse.ArgumentParser(description="Minimal GitHub GET test")
    argp.add_argument("endpoint", help="REST endpoint starting with / e.g. /rate_limit")
    argp.add_argument("--kvs", nargs="*", default=[], help="extra query params k=v")
    args = argp.parse_args()

    extra = dict(kv.split("=", 1) for kv in args.kvs)
    gh = GitHubClient()

    for idx, obj in enumerate(gh.get(args.endpoint, **extra)):
        print(json.dumps(obj, indent=2)[:700])
        if idx == 2:
            break
