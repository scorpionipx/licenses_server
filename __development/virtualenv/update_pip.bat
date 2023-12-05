@echo off
color A
cls


SET TOOL_NAME=ScorpionIPX Python Virtualenv PIP Updater v3.0.0
echo %TOOL_NAME%


set /P VIRTUALENV_SUFFIX=<.path


@cd /d "%~dp0"
cd ..
cd ..
set BASE_DIR=%cd%
echo Using base dir: %BASE_DIR%


set VIRTUALENV=%BASE_DIR%\%VIRTUALENV_SUFFIX%
echo Using virtual environment: %VIRTUALENV%
echo Using virtualenv: %VIRTUALENV%


%VIRTUALENV% -V
echo.
pause


%VIRTUALENV% -m pip install %module_name% -U pip

pause
