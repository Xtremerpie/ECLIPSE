@echo off
title ECLIPSE UNKNOWN SYSTEM ULTIMATE
cd /d "%~dp0"
python ECLIPSE_ULTIMATE.py
if errorlevel 1 (
 echo.
 echo ECLIPSE could not start. Make sure Python 3 is installed.
 pause
)
