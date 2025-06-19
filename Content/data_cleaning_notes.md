# Data Cleaning and Normalization Notes

> Objective: Transform raw JSON responses from GitHub into simple DataFrames for exploration.

---

## 1 · Search Repositories → `repos_df`

### Fields Used

- `full_name`
- `stargazers_count`
- `language`

### Transformations

| Step | Description |
|------|-------------|
| 1    | Flattened raw JSON into a flat table with `pandas.DataFrame()`. |
| 2    | Selected key fields for display: repository name, stars, and language. |
| 3    | No filtering, sorting, or missing value handling was applied. |

```python
repos_df = pd.DataFrame(repos)[['full_name', 'stargazers_count', 'language']]
```

---

## 2 · Commits → `commits_df`

### Fields Used

- `sha`
- `commit.author.name`
- `commit.message`

### Transformations

| Step | Description |
|------|-------------|
| 1    | Flattened nested commit object with `pd.json_normalize()`. |
| 2    | Selected basic metadata: commit SHA, author name, message. |
| 3    | No time conversion or deduplication performed. |

```python
commits_df = pd.json_normalize(commits)[['sha', 'commit.author.name', 'commit.message']]
```

---

## 3 · Repository Contents → `contents_df`

### Fields Used

- `name`
- `type`
- `size`

### Transformations

| Step | Description |
|------|-------------|
| 1    | Parsed JSON directly into a DataFrame. |
| 2    | Selected fields relevant for basic listing: file name, type (file/folder), and size. |

```python
contents_df = pd.DataFrame(contents)[['name', 'type', 'size']]
```

---

## Notes

- **Pagination** was handled via the helper `paginated_get()` for all endpoints.
- **No null handling** or schema validation was included in this prototype.
- **No writes** to disk (CSV or Parquet) are performed in the current version.

---

*Updated: 18 Jun 2025*