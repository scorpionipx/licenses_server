@ECHO off
COLOR A
CLS


SET TOOL_NAME=ScorpionIPX Python Virtualenv Module Installer v4.0.0
ECHO %TOOL_NAME%
ECHO.


SET /P VIRTUALENV_SUFFIX=<.path


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


%VIRTUALENV% -V
ECHO.

GOTO HELP

:INSTALL_MODULE
ECHO Enter module's name!
SET /P module_name=module: 

IF %module_name% == exit GOTO EXIT_MODULE_INSTALLER

IF %module_name% == h GOTO HELP
IF %module_name% == help GOTO HELP

%VIRTUALENV% -m pip install %module_name%


GOTO INSTALL_MODULE

:HELP
ECHO HELP MENU
ECHO.
ECHO COMMANDS:
ECHO h , help - Prompts %TOOL_NAME% HELP MENU
ECHO exit - Quits %TOOL_NAME%
ECHO.
GOTO INSTALL_MODULE

:EXIT_MODULE_INSTALLER
ECHO.
ECHO Thank you for using %TOOL_NAME%
pause
