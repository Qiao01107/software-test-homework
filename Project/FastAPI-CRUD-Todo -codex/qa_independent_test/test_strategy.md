# Independent Test Strategy

## Scope and assumptions

The repository is a small REST API with no authentication, external service, frontend, CI configuration, or tracked automated tests. The strategy therefore prioritizes observable API contracts and persistence behavior over browser or performance testing. No business source file is modified.

## Test levels

1. **API/integration:** FastAPI `TestClient` invokes the real application routes, Pydantic validation, SQLAlchemy ORM, and SQLite database. Each test receives an isolated in-memory database through the existing `get_db` dependency override.
2. **Focused unit:** The existing database generator is checked for session cleanup with a stub session. This is limited to a resource-lifecycle behavior not observable through the overridden API fixture.
3. **Defect probe:** A separate test intentionally fails when the observed response violates the expected API contract, so the defect is visible without changing production code.

## Risk-based priorities

CRUD persistence and request/response validation are high priority because they are the product's core behavior and can corrupt or make data unreadable. Missing-resource errors and pagination boundaries are medium priority. No auth, third-party, UI, or production-environment tests were invented because the repository exposes none of those surfaces.

## Exit criteria

- All normal regression tests pass.
- Every endpoint has a happy path and at least one error path where applicable.
- Response shape and JSON content type are asserted on representative responses.
- Coverage is reported with branch coverage.
- Any failing probe is classified as confirmed defect, pending confirmation, test-script issue, environment issue, or unclear requirement.
