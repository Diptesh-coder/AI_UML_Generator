"""
Configuration Helper Script
Run this to check your setup and configure API keys
"""
import os
import sys
from pathlib import Path


def check_dependencies():
    """Check if all required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
        ("plantuml", "PlantUML renderer"),
        ("pdfplumber", "PDF text extraction"),
        ("docx", "Word document support"),
        ("langchain", "LangChain framework"),
        ("groq", "Groq API client"),
        ("dotenv", "Environment variables"),
    ]
    
    missing = []
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package:20s} - {description}")
        except ImportError:
            print(f"  ❌ {package:20s} - {description}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"   Install with: pip install {' '.join(missing)}")
        return False
    else:
        print("\n✅ All dependencies installed!")
        return True


def check_env_file():
    """Check if .env file exists and is configured"""
    print("\n⚙️  Checking environment configuration...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_example.exists():
        print("  ⚠️  .env.example not found")
        return False
    
    if not env_file.exists():
        print("  ⚠️  .env file not found")
        print("  📝 Creating .env from .env.example...")
        
        with open(env_example, 'r') as src:
            content = src.read()
        
        with open(env_file, 'w') as dest:
            dest.write(content)
        
        print("  ✅ Created .env file")
        print("  ⚠️  Please edit .env and add your Groq API key")
        return False
    
    # Check if API key is configured
    with open(env_file, 'r') as f:
        content = f.read()
    
    if 'your_groq_api_key_here' in content:
        print("  ⚠️  Groq API key not configured in .env")
        print("  📝 Edit .env and replace 'your_groq_api_key_here' with your actual key")
        print("  🔗 Get your key at: https://console.groq.com/keys")
        return False
    
    print("  ✅ .env file configured")
    return True


def check_directories():
    """Check if necessary directories exist"""
    print("\n📁 Checking directories...")
    
    directories = [
        "static",
        "templates",
        "uploads",
        "outputs",
        "sessions"
    ]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            print(f"  📁 Creating {dir_name}/")
            dir_path.mkdir(exist_ok=True)
        else:
            print(f"  ✅ {dir_name}/ exists")
    
    return True


def test_groq_connection():
    """Test if Groq API is accessible"""
    print("\n🔌 Testing Groq connection...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key or api_key == "your_groq_api_key_here":
            print("  ⚠️  Groq API key not configured")
            print("  ℹ️  The system will work in rule-based mode")
            return False
        
        try:
            from langchain_groq import ChatGroq
            
            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=100
            )
            
            # Test with a simple query
            response = llm.invoke("Say 'OK' if you receive this message.")
            print(f"  ✅ Groq API connected successfully!")
            print(f"  📝 Test response: {response.content[:50]}...")
            return True
            
        except Exception as e:
            print(f"  ❌ Groq API error: {str(e)}")
            print(f"  ℹ️  Check your API key and internet connection")
            return False
    
    except Exception as e:
        print(f"  ❌ Configuration error: {str(e)}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("🔧 AI UML Diagram Generator - Setup Checker")
    print("=" * 60)
    
    deps_ok = check_dependencies()
    dirs_ok = check_directories()
    env_ok = check_env_file()
    
    if deps_ok and env_ok:
        groq_ok = test_groq_connection()
    else:
        groq_ok = False
    
    print("\n" + "=" * 60)
    print("📊 Setup Summary")
    print("=" * 60)
    print(f"Dependencies:        {'✅ OK' if deps_ok else '❌ Missing'}")
    print(f"Directories:         {'✅ OK' if dirs_ok else '❌ Error'}")
    print(f"Environment (.env):  {'✅ OK' if env_ok else '⚠️  Needs config'}")
    print(f"Groq Connection:     {'✅ OK' if groq_ok else '⚠️  Fallback mode'}")
    print("=" * 60)
    
    if deps_ok and dirs_ok:
        print("\n✅ Basic setup complete!")
        print("🚀 You can start the server with: python app.py")
        
        if not groq_ok:
            print("\nℹ️  Running in RULE-BASED mode (still functional)")
            print("💡 To enable LLM features:")
            print("   1. Get API key from: https://console.groq.com/keys")
            print("   2. Edit .env file")
            print("   3. Add: GROQ_API_KEY=gsk_your_key_here")
            print("   4. Restart the server")
    else:
        print("\n⚠️  Setup incomplete. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
