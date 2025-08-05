#!/usr/bin/env python3
"""
Kustomize Builder Web App Launcher
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        return False
    
    # Check if required packages are installed
    try:
        import flask
        import yaml
        print("✅ Python dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False
    
    # Check if kustomize is installed
    try:
        result = subprocess.run(['kustomize', 'version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Kustomize found: {result.stdout.strip()}")
        else:
            print("❌ Kustomize is not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Kustomize not found! Please install it:")
        print("   Windows: choco install kustomize")
        print("   macOS: brew install kustomize")
        print("   Linux: sudo snap install kustomize")
        return False
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies!")
        return False

def main():
    """Main launcher function"""
    print("🚀 Kustomize Builder Web App Launcher")
    print("=" * 50)
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies. Please install manually:")
            print("   pip install -r requirements.txt")
            return
    
    print("\n🌐 Starting the web application...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the application")
    print("=" * 50)
    
    # Start the Flask application
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main() 