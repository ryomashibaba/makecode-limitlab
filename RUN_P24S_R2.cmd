@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -NoLogo -STA -ExecutionPolicy Bypass -File "%~dp0tools\RUN_P24S_R2.ps1"
set "RESULT=%ERRORLEVEL%"
echo.
echo P2.4S R2 exit code %RESULT%. Previous run records are preserved.
pause
exit /b %RESULT%
