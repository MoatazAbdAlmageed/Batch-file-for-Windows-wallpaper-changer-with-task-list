@echo off
setlocal enabledelayedexpansion

REM ====================================================================
REM Task Wallpaper Updater
REM This script reads tasks from _todo.txt, randomly picks a wallpaper
REM from _wallpapers folder, overlays tasks on it, and sets as wallpaper
REM ====================================================================

REM Set your paths here
set "TODO_FILE=%~dp0_todo.txt"
set "WALLPAPERS_DIR=%~dp0_wallpapers"
set "PYTHON_SCRIPT=%WALLPAPERS_DIR%\create_wallpaper.py"
set "OUTPUT_IMAGE=%WALLPAPERS_DIR%\wallpaper_with_tasks.jpg"

REM Check if _todo.txt exists
if not exist "%TODO_FILE%" (
    echo Error: _todo.txt not found!
    pause
    exit /b 1
)

REM Check if _wallpapers directory exists
if not exist "%WALLPAPERS_DIR%" (
    echo Error: _wallpapers directory not found!
    echo Please create a _wallpapers folder and add your wallpaper images.
    pause
    exit /b 1
)

REM Check if Python script exists
if not exist "%PYTHON_SCRIPT%" (
    echo Error: create_wallpaper.py not found in _wallpapers directory!
    echo Please make sure create_wallpaper.py is in the _wallpapers folder.
    pause
    exit /b 1
)

REM Run the Python script
echo Creating wallpaper with tasks...
python "%PYTHON_SCRIPT%"

if errorlevel 1 (
    echo Error: Failed to create wallpaper. Make sure Python and Pillow are installed.
    echo Install Pillow with: pip install Pillow
    pause
    exit /b 1
)

REM Create PowerShell script to set wallpaper
echo Setting wallpaper...
(
echo Add-Type -TypeDefinition @"
echo using System.Runtime.InteropServices;
echo public class Wallpaper {
echo     [DllImport("user32.dll", CharSet=CharSet.Auto^)]
echo     public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni^);
echo }
echo "@
echo [Wallpaper]::SystemParametersInfo(20, 0, "%OUTPUT_IMAGE%", 3^)
) > "%~dp0set_wallpaper.ps1"

powershell -ExecutionPolicy Bypass -File "%~dp0set_wallpaper.ps1"

if errorlevel 1 (
    echo Warning: Failed to set wallpaper automatically.
    echo You can manually set the wallpaper from: %OUTPUT_IMAGE%
)

echo.
echo ====================================================================
echo Wallpaper updated successfully!
echo Output: %OUTPUT_IMAGE%
echo Tasks source: _todo.txt
echo ====================================================================
