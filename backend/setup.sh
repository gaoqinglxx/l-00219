#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EMBED_DIR="$DIR/embedded_python"
PYTHON_ZIP="$DIR/python.zip"
GET_PIP="$DIR/get-pip.py"
PYTHON_EXE="$EMBED_DIR/python.exe"

PYTHON_URL="https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
GET_PIP_URL="https://bootstrap.pypa.io/get-pip.py"

echo "Setting up game environment..."

if [ ! -d "$EMBED_DIR" ]; then
    # 1. Download Python
    echo "Downloading Python Embedded..."
    curl -L $PYTHON_URL -o $PYTHON_ZIP

    # 2. Extract
    echo "Extracting Python..."
    unzip -q $PYTHON_ZIP -d $EMBED_DIR
    rm $PYTHON_ZIP

    # 3. Enable site-packages
    echo "Enabling site-packages..."
    PTH_FILE=$(ls $EMBED_DIR/*._pth | head -n 1)
    if [ -f "$PTH_FILE" ]; then
        # Use sed to uncomment 'import site'
        sed -i 's/#import site/import site/g' "$PTH_FILE"
    fi
fi

# 4. Install pip if missing
if [ ! -f "$EMBED_DIR/Scripts/pip.exe" ] && [ ! -f "$EMBED_DIR/Scripts/pip" ]; then
    echo "Downloading get-pip.py..."
    curl -L $GET_PIP_URL -o $GET_PIP
    
    echo "Installing pip..."
    "$PYTHON_EXE" $GET_PIP --no-warn-script-location
    rm $GET_PIP
fi

# 5. Install Requirements
echo "Installing requirements..."
"$PYTHON_EXE" -m pip install -r "$DIR/requirements.txt" --no-warn-script-location

echo "Setup complete!"
