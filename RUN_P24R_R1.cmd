@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -NoLogo -STA -ExecutionPolicy Bypass -File "%~dp0tools\RUN_P24R_R1.ps1"
set "R1_EXIT=%ERRORLEVEL%"
echo.
echo P2.4R finished with code %R1_EXIT%. Do not reset a USED latch or overwrite evidence.
pause
exit /b %R1_EXIT%
