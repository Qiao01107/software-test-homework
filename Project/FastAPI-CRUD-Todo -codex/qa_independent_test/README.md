# Independent QA Artifacts

This directory contains an independent test run for the FastAPI-CRUD-Todo project. The pre-existing `ai_test_experiment/` directory and its conclusions were intentionally not used as a test baseline.

## Reproduction

The project runtime was unavailable in the default shell. The run used the bundled Python 3.12.14 executable with dependencies installed into the ignored local directories `_deps` and `_deps_compat`. The final compatible runtime used FastAPI 0.95.2, SQLAlchemy 2.0.21, pytest 8.4.2, pytest-cov 6.2.1, httpx 0.24.1, and Pydantic 1.10.26. See `intervention_log.md` for why Pydantic differs from the project pin.

From the repository root:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'qa_independent_test\_deps_compat') + ';' + (Get-Location)
& 'C:\Users\Qiao\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest -c 'qa_independent_test\pytest.ini' 'qa_independent_test\tests\test_api_contract.py' 'qa_independent_test\tests\test_database_dependency.py' -q --cov=main --cov=database --cov=models --cov=routers --cov=schemas --cov-branch --cov-report=term-missing
& 'C:\Users\Qiao\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest -c 'qa_independent_test\pytest.ini' 'qa_independent_test\tests\test_known_defects.py' -q
```

The first command is the clean regression suite. The second is a deliberately failing defect probe.

See `final_summary.md` for the final conclusion, `defects.md` for classifications, and `raw_*.log` for original command output.
