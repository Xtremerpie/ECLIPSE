@echo off
setlocal
cd /d "%~dp0"
title ECLIPSE 2.0
echo.
echo  ==========================================
echo          E C L I P S E   2.0
echo          THE COMPLETE SYSTEM
echo  ==========================================
echo.
where py >nul 2>nul
if %errorlevel%==0 (
  py -3.14 -m eclipse_v1
  if not errorlevel 1 goto end
  py -3 -m eclipse_v1
  if not errorlevel 1 goto end
)
where python >nul 2>nul
if %errorlevel%==0 (
  python -m eclipse_v1
  if not errorlevel 1 goto end
)
echo.
echo ECLIPSE could not start.
echo Install Python 3.10+ with Tkinter, then run this file again.
echo You can also run: py -3.14 -m eclipse_v1
pause
:end
endlocal
