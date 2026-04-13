Write-Host "[BUILD] Starting build..." -ForegroundColor Cyan
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) { pip install pyinstaller }
pyinstaller --onefile source/main.py
Copy-Item dist\main.exe release\GRAZYNA_DIAGNOSTIC_SUITE.exe -Force
Write-Host "[BUILD] Done." -ForegroundColor Green
