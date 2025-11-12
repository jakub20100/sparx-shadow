#!/usr/bin/env python3
"""
Sparx Shadow Setup Script
Automated installation and configuration tool
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class SparxShadowSetup:
    def __init__(self):
        self.system = platform.system()
        self.python_version = sys.version_info
        self.errors = []
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        print("🔍 Checking Python version...")
        if self.python_version < (3, 8):
            self.errors.append(f"Python 3.8+ required, found {self.python_version.major}.{self.python_version.minor}")
            return False
        print(f"✅ Python {self.python_version.major}.{self.python_version.minor} is compatible")
        return True
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing Python dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to install dependencies: {e}")
            return False
    
    def install_tesseract(self):
        """Install Tesseract OCR based on system"""
        print("📖 Installing Tesseract OCR...")
        
        if self.system == "Windows":
            return self._install_tesseract_windows()
        elif self.system == "Darwin":  # macOS
            return self._install_tesseract_macos()
        elif self.system == "Linux":
            return self._install_tesseract_linux()
        else:
            self.errors.append(f"Unsupported operating system: {self.system}")
            return False
    
    def _install_tesseract_windows(self):
        """Install Tesseract on Windows"""
        print("⚠️  Windows Tesseract installation requires manual steps:")
        print("   1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   2. Install to default location")
        print("   3. Add to PATH environment variable")
        print("   4. Restart your terminal/IDE")
        
        # Check if Tesseract is already installed
        if shutil.which("tesseract"):
            print("✅ Tesseract is already installed and in PATH")
            return True
        
        # Common installation paths
        common_paths = [
            "C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
            "C:\\Users\\%USERNAME%\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"
        ]
        
        for path in common_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                print(f"✅ Tesseract found at: {expanded_path}")
                return True
        
        self.errors.append("Tesseract not found. Please install manually.")
        return False
    
    def _install_tesseract_macos(self):
        """Install Tesseract on macOS"""
        try:
            # Check if Homebrew is available
            if not shutil.which("brew"):
                print("📦 Installing Homebrew...")
                subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', 
                             shell=True, check=True)
            
            # Install Tesseract
            subprocess.run(["brew", "install", "tesseract"], check=True)
            print("✅ Tesseract installed successfully on macOS")
            return True
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to install Tesseract on macOS: {e}")
            return False
    
    def _install_tesseract_linux(self):
        """Install Tesseract on Linux"""
        try:
            # Try apt-get (Debian/Ubuntu)
            if shutil.which("apt-get"):
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "tesseract-ocr"], check=True)
            
            # Try yum (RHEL/CentOS)
            elif shutil.which("yum"):
                subprocess.run(["sudo", "yum", "install", "-y", "tesseract"], check=True)
            
            # Try dnf (Fedora)
            elif shutil.which("dnf"):
                subprocess.run(["sudo", "dnf", "install", "-y", "tesseract"], check=True)
            
            else:
                self.errors.append("No supported package manager found for Linux")
                return False
            
            print("✅ Tesseract installed successfully on Linux")
            return True
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to install Tesseract on Linux: {e}")
            return False
    
    def check_chrome_installation(self):
        """Check if Chrome is installed"""
        print("🔍 Checking Chrome installation...")
        
        chrome_paths = {
            "Windows": [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            ],
            "Darwin": [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            ],
            "Linux": [
                "/usr/bin/google-chrome",
                "/usr/bin/google-chrome-stable",
                "/usr/bin/chromium-browser"
            ]
        }
        
        paths = chrome_paths.get(self.system, [])
        for path in paths:
            if os.path.exists(path):
                print(f"✅ Chrome found at: {path}")
                return True
        
        print("⚠️  Chrome not found. Please install Google Chrome:")
        print("   https://www.google.com/chrome/")
        return False
    
    def create_env_file(self):
        """Create environment configuration file"""
        print("⚙️  Creating environment configuration...")
        
        env_content = f"""# Sparx Shadow Configuration
# Generated on {platform.platform()}

# Flask Configuration
FLASK_SECRET_KEY={os.urandom(32).hex()}
FLASK_ENV=development
FLASK_DEBUG=True

# Tesseract Configuration
TESSERACT_PATH={self._get_tesseract_path()}

# Application Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
"""
        
        try:
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ Environment file created")
            return True
        except Exception as e:
            self.errors.append(f"Failed to create .env file: {e}")
            return False
    
    def _get_tesseract_path(self):
        """Get Tesseract executable path"""
        if self.system == "Windows":
            return "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        else:
            return "/usr/bin/tesseract"
    
    def create_directories(self):
        """Create necessary directories"""
        print("📁 Creating directories...")
        
        directories = ['uploads', 'logs', 'exports']
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✅ Created directory: {directory}")
            except Exception as e:
                self.errors.append(f"Failed to create directory {directory}: {e}")
                return False
        
        return True
    
    def run_tests(self):
        """Run basic tests to verify installation"""
        print("🧪 Running verification tests...")
        
        try:
            # Test imports
            import sympy
            import numpy
            import PIL
            import cv2
            
            # Test Tesseract
            import pytesseract
            
            print("✅ All Python imports successful")
            
            # Test basic functionality
            import sympy as sp
            x = sp.Symbol('x')
            result = sp.solve(x**2 - 4, x)
            print(f"✅ SymPy test: Solutions to x² - 4 = 0 are {result}")
            
            return True
        
        except Exception as e:
            self.errors.append(f"Test failed: {e}")
            return False
    
    def print_summary(self):
        """Print installation summary"""
        print("\n" + "="*60)
        print("SPARX SHADOW SETUP SUMMARY")
        print("="*60)
        
        if not self.errors:
            print("🎉 Setup completed successfully!")
            print("\nNext steps:")
            print("1. Run the application: python app.py")
            print("2. Open browser: http://localhost:5000")
            print("3. Login with your Sparx Maths credentials")
            print("4. Configure bot settings and start automation")
            
            # Create start script
            self.create_start_script()
            
        else:
            print("❌ Setup completed with errors:")
            for error in self.errors:
                print(f"   • {error}")
            
            print("\nPlease fix the errors above and run setup again.")
    
    def create_start_script(self):
        """Create a start script for easy launching"""
        if self.system == "Windows":
            script_content = """@echo off
echo Starting Sparx Shadow...
python app.py
pause
"""
            with open("start.bat", "w") as f:
                f.write(script_content)
            print("\n📄 Created start.bat for easy launching")
        
        else:
            script_content = """#!/bin/bash
echo "Starting Sparx Shadow..."
python3 app.py
"""
            with open("start.sh", "w") as f:
                f.write(script_content)
            os.chmod("start.sh", 0o755)
            print("\n📄 Created start.sh for easy launching")

def main():
    """Main setup function"""
    print("🚀 SPARX SHADOW SETUP")
    print("="*60)
    
    setup = SparxShadowSetup()
    
    # Run setup steps
    steps = [
        setup.check_python_version,
        setup.install_dependencies,
        setup.install_tesseract,
        setup.check_chrome_installation,
        setup.create_env_file,
        setup.create_directories,
        setup.run_tests
    ]
    
    success_count = 0
    for step in steps:
        try:
            if step():
                success_count += 1
            print()
        except Exception as e:
            setup.errors.append(f"Unexpected error in {step.__name__}: {e}")
            print(f"❌ Error in {step.__name__}: {e}\n")
    
    # Print summary
    setup.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if success_count == len(steps) else 1)

if __name__ == "__main__":
    main()