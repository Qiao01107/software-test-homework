# Test Environment and Script Intervention Log

Date: 2026-10-06 (Asia/Shanghai)

1. The default shell had no `python`, `py`, or `pytest` command. The bundled Python 3.12.14 runtime was located at `C:\Users\Qiao\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`.
2. Test dependencies were added under `qa_independent_test\_deps`; the project requirements were also installed there. This did not modify `requirements.txt` or business source.
3. The first import attempt failed before tests because the pinned `pydantic==1.10.12` is incompatible with Python 3.12's `typing.ForwardRef` signature. This is classified as an environment/reproducibility issue.
4. Upgrading that first target to Pydantic 1.10.15 was insufficient. A clean `qa_independent_test\_deps_compat` target was then created with the same project versions except `pydantic>=1.10.16,<2`, which resolved to 1.10.26. This was a test-only compatibility workaround and is not a proposed business dependency change.
5. Installing project and test requirements into one target in separate commands produced overwrite warnings for shared packages (`h11`, `anyio`, and related files). A clean compatibility target and explicit `h11==0.14.0` resolution were used for the final run. The warning was treated as a test-environment script issue, not a product defect.
6. A package marker `qa_independent_test\__init__.py` was added so the defect probe's relative test import is collected consistently by pytest.

7. A final collection check initially exposed that `pytest.ini` used a path relative to the repository root even though pytest resolves `testpaths` from the configuration root. It therefore scanned dependency test files and the pre-existing experiment directory. The original output is preserved in `raw_collect_check.log`; `testpaths` was corrected to `tests`, and a clean collection check was rerun from `qa_independent_test`.

Original evidence: `raw_import_check.log`, `raw_import_check_compat.log`, `raw_dependency_install.log`, `raw_baseline_run.log`, and `raw_compat_run.log`.
