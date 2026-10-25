@echo off
setlocal

cd /d "%~dp0"
set "PYTHON=python"
if exist "venv\Scripts\python.exe" set "PYTHON=venv\Scripts\python.exe"

"%PYTHON%" -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller is not installed for "%PYTHON%".
    echo Install it with: "%PYTHON%" -m pip install pyinstaller
    exit /b 1
)

"%PYTHON%" -m PyInstaller --noconfirm --clean --onefile --windowed ^
    --name "foczka-hs3-0h-hackathon" ^
    --add-data "app.py;." ^
    --add-data "discourse.py;." ^
    --add-data "assets;assets" ^
    app.py
if errorlevel 1 exit /b 1

echo.
echo Build complete: dist\foczka-hs3-0h-hackathon.exe
