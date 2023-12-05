@ECHO OFF
COLOR A
CLS


SET TOOL_NAME=ScorpionIPX Python Virtualenv PIP Freeze v4.0.0
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


%VIRTUALENV% -V
ECHO.


PUSHD %~dp0
%VIRTUALENV% -m pip freeze > freeze.ipx

PAUSE
