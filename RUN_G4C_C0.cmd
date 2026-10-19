@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -NoLogo -STA -ExecutionPolicy Bypass -File "%~dp0tools\RUN_G4C_C0.ps1"
set "RESULT=%ERRORLEVEL%"
echo.
echo G4C C0 exit code %RESULT%. Previous run records are preserved.
pause
exit /b %RESULT%
