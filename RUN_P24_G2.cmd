@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -NoLogo -STA -ExecutionPolicy Bypass -File "%~dp0tools\P24_G2_ONE_CLICK.ps1" -Mode Prepare
set "G2_RESULT=%ERRORLEVEL%"
echo.
echo G2 finished with code %G2_RESULT%.
echo Historical evidence was NOT reset. No Minecraft command was sent.
pause
exit /b %G2_RESULT%
