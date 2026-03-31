# Setup script for Windows
$ErrorActionPreference = "Stop"

$WorkDir = $PSScriptRoot
$EmbeddedDir = Join-Path $WorkDir "embedded_python"
$PythonZip = Join-Path $WorkDir "python.zip"
$GetPip = Join-Path $WorkDir "get-pip.py"
$PythonExe = Join-Path $EmbeddedDir "python.exe"

$PythonUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
$GetPipUrl = "https://bootstrap.pypa.io/get-pip.py"

Write-Host "Setting up game environment..."

if (-not (Test-Path $EmbeddedDir)) {
    # 1. Download Python
    Write-Host "Downloading Python Embedded..."
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $PythonUrl -OutFile $PythonZip

    # 2. Extract
    Write-Host "Extracting Python..."
    Expand-Archive -Path $PythonZip -DestinationPath $EmbeddedDir -Force
    Remove-Item $PythonZip

    # 3. Enable site-packages (Modify ._pth file)
    $PthFile = Get-ChildItem $EmbeddedDir -Filter "*._pth" | Select-Object -First 1
    if ($PthFile) {
        $Content = Get-Content $PthFile.FullName
        $Content = $Content -replace "#import site", "import site"
        Set-Content $PthFile.FullName $Content
        Write-Host "Enabled site-packages."
    }
}

# 4. Install pip if missing
if (-not (Test-Path (Join-Path $EmbeddedDir "Scripts\pip.exe"))) {
    Write-Host "Downloading get-pip.py..."
    Invoke-WebRequest -Uri $GetPipUrl -OutFile $GetPip
    
    Write-Host "Installing pip..."
    & $PythonExe $GetPip --no-warn-script-location
    Remove-Item $GetPip
}

# 5. Install Requirements
Write-Host "Installing requirements..."
& $PythonExe -m pip install -r (Join-Path $WorkDir "requirements.txt") --no-warn-script-location

Write-Host "Setup complete!"
