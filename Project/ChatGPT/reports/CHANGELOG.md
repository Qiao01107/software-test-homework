# Test environment and script changes

- **E0 — baseline setup**: Original ZIP unpacked to `original/FastAPI-CRUD-Todo`. Unmodified application Python files copied to `working/app`; no original `todo.db` copied into the test runtime. Every API test creates a separate SQLite file via `tmp_path` and overrides only the `get_db` dependency. Production SQLAlchemy model and API handlers remain unchanged.
- **E1 — dependency installation blocked**: Attempted a separate virtual environment with `fastapi==0.95.2`, `sqlalchemy==2.0.21`, `uvicorn==0.22.0`, compatible `httpx==0.24.1`, `pydantic==1.10.24` (modern patch instead of pinned 1.10.12 because local interpreter is Python 3.13), plus pytest tooling. Package index inaccessible (DNS resolution failure), installation not completed. No application file modified. Real tests therefore execute on preinstalled Python 3.13.5 / FastAPI 0.128.2 / Pydantic 2.13.5 / SQLAlchemy 2.0.50 / httpx 0.28.1 / pytest 9.0.2.
- **E2 — original runtime incompatibility risk**: FastAPI/Pydantic warn of deprecated `orm_mode` and `.dict()` with current stack. This environment mismatch is documented as an **environment limitation**, not a confirmed defect in the pinned app stack. Test logic asserts only supported behaviors and records failures transparently.

Further corrections (if any) will be appended here, preserving both initial and final runs.
