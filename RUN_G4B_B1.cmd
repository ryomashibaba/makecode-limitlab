@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -NoLogo -STA -ExecutionPolicy Bypass -File "%~dp0tools\RUN_G4B_B1.ps1"
set "RESULT=%ERRORLEVEL%"
echo.
echo G4B A1 exit code %RESULT%. Previous run records are preserved.
pause
exit /b %RESULT%
