@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Usage: release.bat [patch|minor|major] [optional notes]

set BUMP=%1
if "%BUMP%"=="" set BUMP=patch

set NOTES=%~2
if "%NOTES%"=="" set NOTES=Auto build

powershell -NoProfile -ExecutionPolicy Bypass -File tools\release.ps1 -Bump %BUMP% -Notes "%NOTES%"

endlocal
