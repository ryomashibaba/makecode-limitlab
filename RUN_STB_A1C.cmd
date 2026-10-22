@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0tools\STB_A1C_COPY.ps1"
set "RESULT=%ERRORLEVEL%"
echo.
echo STB A1C copy exit: %RESULT%. No world construction was started.
pause
exit /b %RESULT%
