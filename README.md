# Data‑Source‑API‑Analyst — Practical Work

> **Purpose:** public repository with the solution to the technical exercise for the position of **Data Source API Analyst**. Here you will find documentation on the approach, the code for extracting information from the GitHub API, and the requested artifacts (Postman Collection / Colab Notebook).
---

## 1 · Preliminary research and testing

| What to do | How to do it | Quick reference |
|-----------|--------------|-------------------|
| **1.1 Understand customer needs** | • List the three required reports: **Search Repositories**, **Commits**, and **Contents**.<br>• For each one, note possible filters/relevant data (language, *owner*, date, branch, file path, etc.). |  |
| **1.2 Find the right endpoints** | • `GET /search/repositories` — public search.<br>• `GET /repos/{owner}/{repo}/commits` — commit history.<br>• `GET /repos/{owner}/{repo}/contents/{path}` — file and folder contents.
| [GitHub REST API v3](https://docs.github.com/en/rest) |
| **1.3 Take note of** | • **Authentication:** token personal (PAT) → encabezado `Authorization: Bearer <TOKEN>` + `X‑GitHub‑Api‑Version: 2022‑11‑28` (o el más reciente).<br>• **Paginación:** parámetro `per_page` (máx. 100) + cabecera `Link`.<br>• **Rate limit:** 60 req/h sin token, 5 000 req/h con token; endpoint de control `GET /rate_limit`.<br>• **Errores comunes:** `401` (Unauthorized), `403` (Rate‑limit), `422` (Validation). |  |

---

## 2 · Repository structure

```
├── README.md                 # this guide
├── Content                   # API documentation and utilities
│   ├── api_reference.md
│   ├── error_and_rate_handling.md
│   ├── data_cleaning_notes.md
│   └── github_api_utils.py
├── Postman_Collection        # exported collection
│   └── github_api_test.postman_collection.json
└── Colab                     # optional notebook (bonus)
    └── github_api_test.ipynb
```

---

## 3 · Prerequisites

- GitHub account and **PAT** with minimum `public_repo` permissions.
- Postman (v10+) **or** Google Colab with Python 3.10 + `requests`, `pandas`.
- Internet connection to make calls to `https://api.github.com`.

> **⚠️ Security:** the token should **NOT** be uploaded to the repository. Use environment variables in Postman or Colab *Secrets*. Prerequisites

---

## 4 ·  Next steps (roadmap)

1. **Configure** environment variables/secrets for authentication.
2. **Build** the Postman collection/Colab notebook with pagination and rate limit handling.
3. **Document** the endpoints used, examples, and responses in `api_reference.md`.
4. **Record** best practices for error handling in `error_and_rate_handling.md`.
5. **Clean and normalize** the data (`data_cleaning_notes.md`).
6. **Export** the final artifacts (Postman JSON, Colab `.ipynb`) and push.

---

# 5 · Reflection
This exercise provided a valuable opportunity to deepen my understanding of the GitHub REST API and its practical constraints, such as pagination, rate limits, and data normalization challenges.

Key lessons learned include:

The importance of building reusable API wrappers to streamline repetitive requests.

How to manage rate-limiting programmatically, both in Python and Postman.

The value of clear documentation when working on technical deliverables for non-technical audiences.

Challenges encountered:

Navigating inconsistencies in API responses (e.g., nested fields, nullable authors).

Handling large datasets within time and quota constraints.

Future improvements could include:

Adding unit tests to validate each helper function.

Supporting retries with exponential backoff for greater robustness.

Exploring GitHub GraphQL API for more flexible queries and reduced over-fetching.

---

**Autor:** Mauricio Meza

<sub>Last update: 18 Jun 2025</sub>