@echo off
echo Stopping all Python processes...
taskkill /F /IM python.exe /T
echo.
echo cleanup successful. Please run 'python app.py' now.
pause
