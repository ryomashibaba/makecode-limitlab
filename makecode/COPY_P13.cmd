@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0COPY_P13.ps1"
if errorlevel 1 (
 echo COPY FAILED. Please send screenshot of this window.
 pause
 exit /b 1
)
pause
