# 复现测试的脚本（PowerShell）
# 用法：在项目根目录执行： powershell -ExecutionPolicy Bypass -File ai_test_experiment/run_tests.ps1
$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Py = "D:\CodeTools\conda_envs\todo_test\python.exe"

if (-not (Test-Path $Py)) {
    Write-Error "未找到测试环境 Python：$Py"
}

$env:PYTHONPATH = $ProjectRoot
Set-Location $ProjectRoot

New-Item -ItemType Directory -Force -Path "ai_test_experiment\raw_logs" | Out-Null

& $Py -m pytest ai_test_experiment/tests -v `
    --basetemp=ai_test_experiment/.pytest_tmp `
    --cov=main --cov=routers --cov=schemas --cov=models --cov=database `
    --cov-branch --cov-report=term-missing `
    --cov-report=html:ai_test_experiment/raw_logs/htmlcov

Write-Host "EXIT=$LASTEXITCODE"