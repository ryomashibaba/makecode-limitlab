@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -NoLogo -STA -ExecutionPolicy Bypass -File "%~dp0tools\RUN_G4C5_A4A1.ps1"
set "RESULT=%ERRORLEVEL%"
echo.
echo G4C5 A4A1 exit code %RESULT%. Previous run records are preserved.
pause
exit /b %RESULT%
