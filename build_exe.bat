@echo off
echo ========================================
echo Building clipnotes
echo ========================================
echo.

REM Create dist folder if it doesn't exist
if not exist "dist" mkdir dist

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building clipnotes.exe...
pyinstaller --clean --distpath=dist --workpath=build clipnotes.spec

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable: dist\clipnotes.exe
echo.
pause

