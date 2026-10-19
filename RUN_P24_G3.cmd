@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -NoLogo -STA -ExecutionPolicy Bypass -File "%~dp0tools\P24_G2_ONE_CLICK.ps1" -Mode Prepare -BundleResult
set "G3_RESULT=%ERRORLEVEL%"
echo.
echo G3 exit code %G3_RESULT%. No reset, retry, or Minecraft command sent from Windows.
pause
exit /b %G3_RESULT%
