@echo off
set "BACKEND_DIR=%~dp0backend"
set "PYTHON_EXE=%BACKEND_DIR%\embedded_python\python.exe"

REM --- Check System Python ---
echo Checking system Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo System Python detected. Checking dependencies...
    python -c "import pygame" >nul 2>&1
    if %errorlevel% equ 0 (
        echo Dependencies satisfied. Starting game with system Python...
        python "%BACKEND_DIR%\main.py"
        if %errorlevel% equ 0 goto :EOF
    ) else (
        echo Dependencies missing. Attempting to install...
        python -m pip install -r "%BACKEND_DIR%\requirements.txt"
        if %errorlevel% equ 0 (
            echo Dependencies installed. Starting game with system Python...
            python "%BACKEND_DIR%\main.py"
            goto :EOF
        )
    )
)

REM --- Fallback to Embedded Python ---
if not exist "%PYTHON_EXE%" (
    echo System Python unavailable or setup failed. Using Embedded Python...
    echo Initializing portable environment...
    powershell -NoProfile -ExecutionPolicy Bypass -File "%BACKEND_DIR%\setup.ps1"
    if errorlevel 1 (
        echo Setup failed!
        pause
        exit /b 1
    )
)

"%PYTHON_EXE%" "%BACKEND_DIR%\main.py"
pause
