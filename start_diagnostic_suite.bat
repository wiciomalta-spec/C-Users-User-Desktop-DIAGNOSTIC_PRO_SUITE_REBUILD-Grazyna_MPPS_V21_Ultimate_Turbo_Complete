@echo off
echo ============================================================
echo DIAGNOSTIC PRO SUITE ULTIMATE EDITION
echo Wersja: 2.0.0
echo ============================================================

cd /d "Grazyna_MPPS_V21_Ultimate_Turbo_Complete"

echo Uruchamianie systemu diagnostycznego...
python CORE/PROFESSIONAL_CONTROL_PANEL.html

if errorlevel 1 (
    echo Błąd uruchamiania systemu!
    pause
    exit /b 1
)

echo System uruchomiony pomyślnie!
pause
