@echo off
echo ============================================================
echo DIAGNOSTIC PRO SUITE ULTIMATE EDITION
echo Instalator: Pomijanie nssm.exe
echo ============================================================

set TARGET=C:\Users\User\Desktop\Grazyna_MPPS_V21_Ultimate_Turbo_Complete

echo Usuwanie katalogu docelowego z pominięciem nssm.exe...

for /f "delims=" %%F in ('dir "%TARGET%" /b /s') do (
    if /i not "%%~nxF"=="nssm.exe" (
        del /f /q "%%F" >nul 2>&1
    )
)

echo Kopiowanie plików...
xcopy "%~dp0Grazyna_MPPS_V21_Ultimate_Turbo_Complete" "%TARGET%" /E /I /Y

echo Instalacja zakonczona.
pause