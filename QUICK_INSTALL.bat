@echo off
echo ============================================================
echo DIAGNOSTIC PRO SUITE ULTIMATE EDITION
echo Quick Install Script v2.0.0
echo ============================================================

echo Sprawdzanie Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo BŁĄD: Python nie jest zainstalowany!
    echo Pobierz Python z: https://python.org
    pause
    exit /b 1
)

echo ✅ Python znaleziony
echo.

echo Instalowanie wymaganych bibliotek...
python -m pip install psutil requests lz4 semver --quiet

echo.
echo Uruchamianie instalatora...
python INSTALL_TO_TARGET_DIRECTORY.py

if errorlevel 1 (
    echo.
    echo ❌ Instalacja nieudana!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 🎉 INSTALACJA ZAKOŃCZONA POMYŚLNIE!
echo ============================================================
echo.
echo System zainstalowany w:
echo C:\Users\User\Desktop\Grazyna_MPPS_V21_Ultimate_Turbo_Complete
echo.
echo Sposoby uruchomienia:
echo 1. START_DIAGNOSTIC_SUITE.bat
echo 2. START_DIAGNOSTIC_SUITE.ps1
echo 3. Skrót na pulpicie
echo 4. http://localhost:8080
echo.
echo ============================================================

set /p choice="Czy uruchomić system teraz? (Y/N): "
if /i "%choice%"=="Y" (
    cd /d "C:\Users\User\Desktop\Grazyna_MPPS_V21_Ultimate_Turbo_Complete"
    START_DIAGNOSTIC_SUITE.bat
)

pause
