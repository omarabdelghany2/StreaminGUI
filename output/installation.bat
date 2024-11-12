@echo off
:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Python...
    :: Download and install Python. Replace the URL below with the correct installer for your OS.
    powershell -Command "Start-Process 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait"
)

:: Verify Python installation
python --version
if %errorlevel% neq 0 (
    echo Python installation failed. Exiting.
    exit /b 1
)

:: Ensure Pip is installed
python -m ensurepip --upgrade
if %errorlevel% neq 0 (
    echo Pip installation failed. Exiting.
    exit /b 1
)

:: Install packages from requirements.txt
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo Environment setup complete.
pause
