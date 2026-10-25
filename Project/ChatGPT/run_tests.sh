#!/usr/bin/env bash
set -uo pipefail
BASE="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$BASE/working/app"
cd "$BASE/working/app" || exit 1
python -m pytest "$BASE/tests" -c "$BASE/pytest.ini" \
  --cov=main --cov=database --cov=models --cov=routers --cov=schemas \
  --cov-branch --cov-report="term-missing:skip-covered" \
  --cov-report="xml:$BASE/reports/coverage.xml" \
  --cov-report="html:$BASE/reports/htmlcov" \
  --junitxml="$BASE/reports/junit_final.xml" \
  2>&1 | tee "$BASE/logs/pytest_final.log"
exit "${PIPESTATUS[0]}"
