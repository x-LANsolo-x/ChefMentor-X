#!/usr/bin/env python3
"""
Test runner script for ChefMentor X backend
"""
import sys
import subprocess

def run_tests():
    """Run all backend tests with coverage"""
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html"
    ]
    
    print("🧪 Running ChefMentor X Backend Tests...")
    print("=" * 60)
    
    result = subprocess.run(cmd, cwd=".")
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("\n❌ Some tests failed. Check output above.")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
