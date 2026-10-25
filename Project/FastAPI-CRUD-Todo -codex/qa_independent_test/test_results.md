# Independent Test Results

Date: 2026-10-06 (Asia/Shanghai)

## Final regression run

- Command: pytest against `test_api_contract.py` and `test_database_dependency.py` with branch coverage.
- Result: **10 passed, 1 warning, exit 0**.
- Warning: Starlette emits a deprecation warning for `anyio.abc.BlockingPortal` under the compatible runtime.
- Coverage: **100% statements/lines and 100% branches** for the measured project modules (`main`, `database`, `models`, `routers`, `schemas`); 83 statements and 8 branches. Function coverage was not emitted by this coverage.py report.
- Reports: `coverage_branch.json`, `coverage_html/`, and `raw_final_regression_coverage_run.log`.

## Defect probe

- Command: pytest against `test_known_defects.py`.
- Result: **1 failed, 1 warning, exit 1**, consistently reproducing D-001.
- Observation: `status=500`, body `Internal Server Error`.
- Report: `raw_final_defect_probe_run.log`.

## Combined baseline

The first compatible run executed 9 tests: 8 passed and the same defect probe failed. After adding coverage-focused checks for database cleanup and missing-resource update handling, the final regression count became 10 passing tests; the defect probe remained isolated and failing.
