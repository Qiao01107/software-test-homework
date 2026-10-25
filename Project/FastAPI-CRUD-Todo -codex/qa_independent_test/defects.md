# Defect Classification

## D-001 — PUT accepts nullable title but returns HTTP 500

- **Classification:** Confirmed defect.
- **Suggested severity:** High; a request accepted by the update schema can persist an unreadable record and produce a server error instead of a client error or valid response.
- **Endpoint:** `PUT /todos/{todo_id}`
- **Precondition:** A todo exists.
- **Steps:** Create `{"title":"Non-null title","description":"groceries"}`; then send `{"title":null}` to the same id.
- **Expected:** The API must either reject the request with a 4xx validation response, or explicitly support clearing the title and return a response whose contract permits null.
- **Observed:** HTTP 500 with body `Internal Server Error`.
- **Evidence:** `tests/test_known_defects.py` and `raw_final_defect_probe_run.log`.
- **Likely cause:** `TodoUpdate.title` is typed `Optional[str]`, so null is accepted and assigned to the ORM row; `TodoOut` inherits a non-null `title: str`. The commit occurs before response-model validation, so the route returns an unhandled response-validation failure.

## Pending confirmation / unclear requirements

- Blank title acceptance is not specified by README or a formal contract.
- Negative `skip`/`limit` behavior is not specified; the source has no non-negative query validation.
- `POST /todos/` returns 200 rather than the common REST 201; the repository does not state which status is required.

These are not counted as confirmed defects in this run.

## Other classifications

- **Test script issue:** Initial dependency installation into a shared target produced package overwrite warnings. The clean compatibility target was used for final evidence.
- **Environment issue:** The exact project pin `pydantic==1.10.12` could not import under the only usable Python 3.12.14 runtime. This prevented an exact-pins run; it was worked around only in the test environment.
