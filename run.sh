#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$DIR/backend"
PYTHON_EXE="$BACKEND_DIR/embedded_python/python.exe"

# 1. Try System Python (Linux/macOS/Git Bash)
if command -v python3 &>/dev/null; then
    PY_CMD="python3"
elif command -v python &>/dev/null; then
    PY_CMD="python"
fi

if [ -n "$PY_CMD" ]; then
    echo "Checking system Python ($PY_CMD)..."
    if $PY_CMD -c "import pygame" &>/dev/null; then
        echo "Dependencies satisfied. Starting with system Python..."
        $PY_CMD "$BACKEND_DIR/main.py"
        exit 0
    else
        echo "Dependencies missing. Attempting to install..."
        $PY_CMD -m pip install -r "$BACKEND_DIR/requirements.txt"
        if [ $? -eq 0 ]; then
            echo "Dependencies installed. Starting..."
            $PY_CMD "$BACKEND_DIR/main.py"
            exit 0
        fi
    fi
fi

# 2. Fallback to Embedded Python (Windows Git Bash only)
# Note: Embedded Python zip is Windows-only.
if [ ! -f "$PYTHON_EXE" ]; then
    echo "System Python unavailable or setup failed. Using Embedded Python..."
    
    if command -v powershell &> /dev/null; then
        # Windows Git Bash
        echo "Initializing portable environment..."
        powershell -NoProfile -ExecutionPolicy Bypass -File "$BACKEND_DIR/setup.ps1"
    else
        # Linux/macOS - Cannot use Windows embedded python
        echo "Error: System Python not found or missing dependencies."
        echo "Please install Python 3.8+ and run: pip install -r backend/requirements.txt"
        exit 1
    fi
fi

"$PYTHON_EXE" "$BACKEND_DIR/main.py"
