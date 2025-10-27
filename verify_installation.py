#!/usr/bin/env python
"""
TryScape Installation Verification Script
Run this script to verify that all dependencies are installed correctly.
"""
import sys


def check_imports():
    """Check if all required packages can be imported."""
    print("Checking required packages...")
    
    required_packages = {
        'flask': 'Flask',
        'openai': 'Azure OpenAI client',
        'PIL': 'Pillow (Image processing)',
        'dotenv': 'python-dotenv',
        'requests': 'Requests',
    }
    
    missing_packages = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - NOT INSTALLED")
            missing_packages.append(name)
    
    return len(missing_packages) == 0


def check_structure():
    """Check if required directories exist."""
    import os
    
    print("\nChecking project structure...")
    
    required_dirs = [
        'app',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/templates',
        'app/utils',
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ - MISSING")
            all_exist = False
    
    return all_exist


def check_env():
    """Check if .env file exists."""
    import os
    
    print("\nChecking configuration...")
    
    if os.path.exists('.env'):
        print("✓ .env file exists")
        return True
    else:
        print("✗ .env file NOT FOUND")
        print("  Please copy .env.example to .env and configure it")
        return False


def main():
    """Run all checks."""
    print("=" * 50)
    print("TryScape Installation Verification")
    print("=" * 50)
    print()
    
    checks = [
        ("Package Dependencies", check_imports),
        ("Project Structure", check_structure),
        ("Configuration", check_env),
    ]
    
    results = []
    for check_name, check_func in checks:
        result = check_func()
        results.append(result)
        print()
    
    print("=" * 50)
    if all(results):
        print("✓ All checks passed!")
        print("\nYou can now run the application with: python run.py")
        return 0
    else:
        print("✗ Some checks failed")
        print("\nPlease fix the issues above and run this script again")
        return 1


if __name__ == '__main__':
    sys.exit(main())
