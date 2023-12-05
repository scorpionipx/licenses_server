@ECHO OFF
COLOR A
CLS


SET TOOL_NAME=ScorpionIPX Django Create Superuser v4.0.0
ECHO %TOOL_NAME%
ECHO.


REM Get script location
PUSHD %~dp0
CD ..
CD ..

SET BASE_DIR=%CD%
ECHO Using base dir: %BASE_DIR%


REM Get virtualenv location
SET /P VIRTUALENV_SUFFIX=<__development\virtualenv\.path
SET VIRTUALENV=%BASE_DIR%\%VIRTUALENV_SUFFIX%
ECHO Using virtual environment: %VIRTUALENV%


SET DJANGO_MANAGER=%BASE_DIR%\manage.py
ECHO Using Django manager: %DJANGO_MANAGER%


ECHO Waiting for user input...
PAUSE


%VIRTUALENV% %DJANGO_MANAGER% createsuperuser
PAUSE
