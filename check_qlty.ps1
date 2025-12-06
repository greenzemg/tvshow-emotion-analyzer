Write-Host ">>> Starting Code Quality Check..." -ForegroundColor Green

# 1. Run isort (Import Sorter)
Write-Host "`n[1/4] Running isort (Import Sorter)..." -ForegroundColor Green
isort backend/ --atomic
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ isort failed." -ForegroundColor Red
    exit 1
}

# 2. Run YAPF (Formatter)
Write-Host "`n[2/4] Running YAPF (Formatter)..." -ForegroundColor Green
# -i: in-place, -r: recursive, -p: parallel
yapf -i -r -p backend/
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ YAPF failed to format code." -ForegroundColor Red
    exit 1
}

# 3. Run Flake8 (Linter)
Write-Host "`n[3/4] Running Flake8 (Linter)..." -ForegroundColor Green
flake8 backend/
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Flake8 failed. Please fix style errors." -ForegroundColor Red
    exit 1
}

# 4. Run Mypy (Type Checker)
Write-Host "`n[4/4] Running Mypy (Type Checker)..." -ForegroundColor Green
mypy backend/
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Mypy failed. Please fix type errors." -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ SUCCESS! All checks passed. You are ready to commit." -ForegroundColor Green
exit 0