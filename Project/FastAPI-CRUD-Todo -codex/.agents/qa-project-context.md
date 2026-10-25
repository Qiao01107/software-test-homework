# QA Project Context — Independent QA Run

## Product
- **Product:** FastAPI-CRUD-Todo
- **Type:** Local REST API service for CRUD management of todo items.
- **Critical flows:** create a todo; list todos; retrieve one todo; update a todo; delete a todo; reject malformed or missing-resource requests.

## Tech Stack
- **Backend:** Python FastAPI 0.95.2.
- **API style:** REST/JSON.
- **Database:** SQLite via SQLAlchemy 2.0.21.
- **Frontend/hosting/CI:** None present in the repository.

## Test Stack
- **Existing project tests:** None tracked in the repository.
- **Independent suite:** pytest with FastAPI TestClient/httpx, configured under `qa_independent_test/`.
- **Coverage:** pytest-cov/coverage.py when available.

## CI/CD
- No CI configuration detected. This run is local and preserves raw command logs.

## Environments
- Test environment is the local bundled Python runtime and an in-memory SQLite database per test.
- The application source uses a file SQLite database by default; tests do not use that database for test data.

## Quality Goals
- Execute all in-scope endpoint happy paths and error paths.
- Report line, branch, and function coverage when the coverage plugin is available.
- Preserve enough raw evidence to reproduce every finding.

## Risk Areas

| Area | Risk | Impact × Likelihood | Notes |
|---|---|---:|---|
| CRUD persistence lifecycle | High | 4 × 3 = 12 | Core user value; state transitions must remain consistent. |
| Request/response validation | High | 4 × 3 = 12 | Invalid payloads can cause data corruption or 5xx responses. |
| Missing-resource/error handling | Medium | 4 × 2 = 8 | Incorrect status codes make clients unable to recover safely. |
| Pagination boundaries | Medium | 3 × 3 = 9 | Unvalidated offsets/limits can produce surprising result sets. |

## Team
- **Test owner for this run:** Independent QA execution by Codex.
- **Known team ratio:** Not provided; record as unknown rather than infer.

## Conventions
- Tests are kept separate from business code in `qa_independent_test/tests/`.
- Each test uses isolated in-memory SQLite data and cleans dependency overrides after execution.
- Tests assert observable API behavior: status, headers, response shape, and state transitions.
