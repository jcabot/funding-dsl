#!/usr/bin/env python3
"""
TextX Tests Runner - Runs all TextX-related tests in sequence.
"""

import sys
import subprocess
from pathlib import Path

def run_test(test_file):
    """Run a single test file and return success status"""
    print(f"\n🧪 Running {test_file.name}...")
    print("-" * 50)
    
    try:
        result = subprocess.run([sys.executable, str(test_file)], 
                              capture_output=True, text=True, cwd=test_file.parent.parent.parent)
        
        if result.returncode == 0:
            print(f"✅ {test_file.name} PASSED")
            return True
        else:
            print(f"❌ {test_file.name} FAILED")
            if result.stdout:
                print("STDOUT:")
                print(result.stdout)
            if result.stderr:
                print("STDERR:")
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running {test_file.name}: {e}")
        return False

def main():
    print("🚀 TextX Test Suite Runner")
    print("=" * 60)
    
    test_dir = Path(__file__).parent
    
    # Test files to run
    test_files = [
        test_dir / "test_textx_parser_fixed.py",
        test_dir / "test_roundtrip_textx.py"
    ]
    
    results = []
    
    for test_file in test_files:
        if test_file.exists():
            success = run_test(test_file)
            results.append((test_file.name, success))
        else:
            print(f"⚠️  Test file not found: {test_file.name}")
            results.append((test_file.name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\n📈 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All TextX tests PASSED!")
        return True
    else:
        print(f"❌ {failed} test(s) FAILED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 