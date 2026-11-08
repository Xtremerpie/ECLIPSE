@echo off
setlocal
cd /d "%~dp0"
echo Starting ECLIPSE V1...
where py >nul 2>nul
if %errorlevel%==0 (
  py -3.14 -m eclipse_v1
  if not errorlevel 1 goto end
  py -m eclipse_v1
  if not errorlevel 1 goto end
)
where python >nul 2>nul
if %errorlevel%==0 (
  python -m eclipse_v1
  if not errorlevel 1 goto end
)
echo.
echo Could not launch Python. Install Python 3.10+ with Tkinter and add it to PATH.
echo On Windows, try: py -3.14 -m eclipse_v1
pause
:end
endlocal
