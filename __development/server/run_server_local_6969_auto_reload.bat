@ECHO OFF
COLOR A
CLS


SET TOOL_NAME=ScorpionIPX Django Run Server Utils v4.0.0
ECHO %TOOL_NAME%
ECHO.
ECHO INFO: Start the server with auto reload feature enabled!


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


%VIRTUALENV% -V
ECHO.


SET DJANGO_MANAGER=%BASE_DIR%\manage.py
ECHO Using Django manager: %DJANGO_MANAGER%


PUSHD %~dp0


SET PORT=6969
%VIRTUALENV% %DJANGO_MANAGER% runserver 0.0.0.0:%PORT%


PAUSE
