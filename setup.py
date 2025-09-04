#!/usr/bin/env python3
"""
MindCare Setup Script
This script helps set up the MindCare mental health support platform
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing packages")
        sys.exit(1)

def setup_environment():
    """Set up environment file"""
    env_file = Path(".env")
    env_template = Path(".env.template")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    if env_template.exists():
        print("\n🔧 Setting up environment file...")
        env_template.rename(env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your actual configuration values")
    else:
        print("❌ .env.template file not found")

def check_firebase_config():
    """Check if Firebase configuration is valid"""
    from dotenv import load_dotenv
    load_dotenv()
    
    firebase_config = os.getenv("FIREBASE_CONFIG_JSON")
    if not firebase_config or firebase_config.startswith("your-"):
        print("⚠️  Please configure your Firebase credentials in .env file")
        return False
    
    try:
        json.loads(firebase_config)
        print("✅ Firebase configuration appears valid")
        return True
    except json.JSONDecodeError:
        print("❌ Invalid Firebase configuration JSON")
        return False

def check_openai_config():
    """Check if OpenAI configuration is valid"""
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or openai_key.startswith("your_"):
        print("⚠️  Please configure your OpenAI API key in .env file")
        return False
    
    print("✅ OpenAI configuration appears valid")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["templates", "static/css", "static/js", "logs"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Created necessary directories")

def main():
    """Main setup function"""
    print("🧠 MindCare Mental Health Platform Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Setup environment
    setup_environment()
    
    # Create directories
    create_directories()
    
    # Load environment and check configurations
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        print("\n🔍 Checking configurations...")
        firebase_ok = check_firebase_config()
        openai_ok = check_openai_config()
        
        print("\n" + "=" * 40)
        print("🎉 Setup completed!")
        
        if not firebase_ok or not openai_ok:
            print("\n⚠️  Configuration needed:")
            print("1. Edit .env file with your actual API keys")
            print("2. Set up Firebase project and add credentials")
            print("3. Get OpenAI API key from https://platform.openai.com")
        
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("\n📖 For more information, see README.md")
        
    except ImportError:
        print("❌ Error: Required packages not installed properly")
        sys.exit(1)

if __name__ == "__main__":
    main()