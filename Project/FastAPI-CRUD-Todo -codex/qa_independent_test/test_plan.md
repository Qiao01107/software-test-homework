# Independent Test Plan

## Coverage map

| ID | Area | Scenario | Result |
|---|---|---|---|
| API-01 | Root | Health message and JSON content type | Pass |
| API-02 | Create | Create todo and default `status=pending` | Pass |
| API-03 | Read | List, fetch, and empty-list behavior | Pass |
| API-04 | Update | Partial update preserves unset fields | Pass |
| API-05 | Delete | Delete removes resource; repeat delete is 404 | Pass |
| API-06 | Validation | Missing title and non-integer path id return 422 | Pass |
| API-07 | Errors | Missing GET and PUT resource return 404 contract | Pass |
| API-08 | Pagination | `skip`/`limit` return the expected slices | Pass |
| DB-01 | Resource lifecycle | `get_db` closes the session after consumption | Pass |
| DEF-01 | Contract consistency | `PUT` with nullable title must not produce an unhandled 500 | Fails; confirmed defect |

## Deferred or unclear requirements

The repository does not specify whether blank titles, negative pagination parameters, or `201 Created` versus the current `200 OK` create response are valid requirements. These are recorded as requirement questions rather than confirmed defects and were not used to fail the regression suite.
