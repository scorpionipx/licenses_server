@echo off
color A
cls

echo ScorpionIPX Django migrate Utils v3.0.0
echo.
echo INFO: this script should be used every time a database update occurs!
REM update virtualenv location
@cd /d "%~dp0"
cd ..
cd ..

set BASE_DIR=%cd%
echo Using base dir: %BASE_DIR%

set /P VIRTUALENV_SUFFIX=<__development\virtualenv\.path
set VIRTUALENV=%BASE_DIR%\%VIRTUALENV_SUFFIX%
echo Using virtual environment: %VIRTUALENV%

set DJANGO_MANAGER=%BASE_DIR%\manage.py
echo Using Django manager: %DJANGO_MANAGER%


echo Waiting for user input...
pause

%VIRTUALENV% %DJANGO_MANAGER% migrate --fake
pause
