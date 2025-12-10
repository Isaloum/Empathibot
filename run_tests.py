#!/usr/bin/env python3
"""
MindCare Test Runner
Choose your testing method based on your setup
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check what dependencies are available"""
    available = {}
    
    try:
        import flask
        available['flask'] = True
    except ImportError:
        available['flask'] = False
    
    try:
        import firebase_admin
        available['firebase'] = True
    except ImportError:
        available['firebase'] = False
    
    try:
        import openai
        available['openai'] = True
    except ImportError:
        available['openai'] = False
    
    return available

def run_demo():
    """Run the standalone demo"""
    print("🚀 Running standalone demo...")
    subprocess.run([sys.executable, "simple_demo.py"])

def run_basic_test():
    """Run basic web interface test"""
    print("🌐 Starting basic web interface test...")
    print("Installing minimal dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "python-dotenv"])
        print("✅ Dependencies installed")
        
        # Create basic .env if it doesn't exist
        if not os.path.exists('.env'):
            with open('.env', 'w') as f:
                f.write("SECRET_KEY=test-secret-key-123\n")
            print("✅ Created basic .env file")
        
        print("\n🌐 Starting basic test server...")
        print("Open your browser to: http://localhost:5000")
        subprocess.run([sys.executable, "test_app_basic.py"])
        
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("Try running: pip3 install flask python-dotenv")

def run_full_test():
    """Run full application test"""
    print("🚀 Starting full application test...")
    
    if not os.path.exists('.env'):
        print("⚠️  No .env file found. Creating from template...")
        if os.path.exists('.env.template'):
            os.rename('.env.template', '.env')
            print("✅ Created .env file from template")
            print("📝 Please edit .env file with your API keys before running the full app")
            return
        else:
            print("❌ No .env.template found. Please create .env file manually")
            return
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed")
        print("\n🚀 Starting full application...")
        print("Open your browser to: http://localhost:5000")
        subprocess.run([sys.executable, "app.py"])
        
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("Try running: pip3 install -r requirements.txt")

def main():
    print("🧠 MindCare Test Runner")
    print("=" * 50)
    
    # Check what's available
    deps = check_dependencies()
    
    print("📋 Available Testing Options:")
    print()
    print("1. 🚀 Standalone Demo (No setup required)")
    print("   - Tests core mental health algorithms")
    print("   - Shows sample analysis results")
    print("   - No web interface")
    print()
    print("2. 🌐 Basic Web Test (Minimal setup)")
    print("   - Full web interface")
    print("   - In-memory database")
    print("   - No external APIs required")
    print()
    print("3. 🌟 Full Application Test (Complete setup)")
    print("   - All features enabled")
    print("   - Firebase + OpenAI integration")
    print("   - WhatsApp bot support")
    print()
    
    # Show current status
    print("📊 Current Setup Status:")
    print(f"   Flask: {'✅' if deps['flask'] else '❌'}")
    print(f"   Firebase: {'✅' if deps['firebase'] else '❌'}")
    print(f"   OpenAI: {'✅' if deps['openai'] else '❌'}")
    print(f"   .env file: {'✅' if os.path.exists('.env') else '❌'}")
    print()
    
    while True:
        choice = input("Choose testing option (1, 2, 3, or 'q' to quit): ").strip()
        
        if choice == 'q':
            print("👋 Goodbye!")
            break
        elif choice == '1':
            run_demo()
            break
        elif choice == '2':
            run_basic_test()
            break
        elif choice == '3':
            run_full_test()
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 'q'")

if __name__ == "__main__":
    main()