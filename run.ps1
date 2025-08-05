# Kustomize Builder Web App Launcher
Write-Host "🚀 Starting Kustomize Builder Web App..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.7 or higher." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Kustomize is installed
try {
    $kustomizeVersion = kustomize version 2>&1
    Write-Host "✅ Kustomize found: $kustomizeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Kustomize not found! Please install Kustomize CLI." -ForegroundColor Red
    Write-Host "Install with: choco install kustomize" -ForegroundColor Yellow
    Write-Host "Or download from: https://github.com/kubernetes-sigs/kustomize/releases" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🌐 Starting the web application..." -ForegroundColor Cyan
Write-Host "Open your browser and go to: http://localhost:5000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

# Start the Flask application
python app.py 