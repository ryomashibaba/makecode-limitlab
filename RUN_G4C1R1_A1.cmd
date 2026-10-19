@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -NoLogo -STA -ExecutionPolicy Bypass -File "%~dp0tools\RUN_G4C1R1_A1.ps1"
set "RESULT=%ERRORLEVEL%"
echo.
echo G4C1R1 A1 exit code %RESULT%. Previous run records are preserved.
pause
exit /b %RESULT%
