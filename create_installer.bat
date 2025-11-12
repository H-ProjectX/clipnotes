@echo off
echo ========================================
echo Creating clipnotes Installer
echo ========================================
echo.

REM Check if Inno Setup is installed
where iscc >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Inno Setup found. Creating installer...
    echo.
    iscc installer.iss
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ========================================
        echo Installer created successfully!
        echo ========================================
        echo.
        echo Installer location: dist\clipnotes_installer.exe
    ) else (
        echo.
        echo ERROR: Failed to create installer
    )
) else (
    echo Inno Setup not found!
    echo.
    echo Please install Inno Setup to create the installer:
    echo 1. Download from: https://jrsoftware.org/isdl.php
    echo 2. Install Inno Setup
    echo 3. Run this script again
    echo.
    echo Or use the portable exe directly: dist\clipnotes.exe
)

echo.
pause

