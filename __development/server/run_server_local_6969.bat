@echo off
color A
cls

echo ScorpionIPX Django run server Utils v3.0.0
echo.
echo INFO: this script should be used to start the server!


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

@cd /d "%~dp0"


set PORT=6969
%VIRTUALENV% %DJANGO_MANAGER% runserver 0.0.0.0:%PORT% --noreload

pause
