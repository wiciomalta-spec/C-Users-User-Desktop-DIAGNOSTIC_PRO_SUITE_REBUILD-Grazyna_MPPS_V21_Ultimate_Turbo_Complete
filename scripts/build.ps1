Write-Host "[BUILD] Starting build..." -ForegroundColor Cyan
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) { pip install pyinstaller }
pyinstaller --onefile source/main.py
if (-not (Test-Path "release")) { New-Item -ItemType Directory -Path "release" | Out-Null }
Copy-Item dist\main.exe release\GRAZYNA_DIAGNOSTIC_SUITE.exe -Force
Write-Host "[BUILD] Done. EXE in .\release" -ForegroundColor Green
Write-Host "[INFO] Aby zbudować instalator NSIS, użyj: makensis.exe installer\grazyna_installer.nsi" -ForegroundColor Yellow
