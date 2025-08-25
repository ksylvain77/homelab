#!/usr/bin/env python3
"""
Quick Test for Homelab Development
Simple smoke test for rapid development feedback
"""

import sys
import os
import requests

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def quick_test():
    """Run quick smoke tests for homelab development"""
    print("🏠 Homelab Quick Test")
    print("==================")
    
    errors = []
    
    # Test 1: Import core modules
    print("📦 Testing module imports...")
    try:
        import modules.system_monitor
        import modules.service_discovery
        print("✅ Core modules import successfully")
    except ImportError as e:
        error = f"❌ Module import failed: {e}"
        print(error)
        errors.append(error)
    
    # Test 2: Basic function calls
    print("🔧 Testing core functions...")
    try:
        from modules.system_monitor import get_cpu_info
        result = get_cpu_info()
        assert 'usage_percent' in result
        assert 'cores' in result
        print("✅ System monitoring functions work")
    except Exception as e:
        error = f"❌ System monitoring test failed: {e}"
        print(error)
        errors.append(error)
    
    # Test 3: Service availability (optional)
    print("🌐 Testing service availability...")
    try:
        response = requests.get("http://localhost:5000/health", timeout=3)
        if response.status_code == 200:
            print("✅ Homelab service is running and responsive")
        else:
            print("⚠️  Homelab service returned non-200 status")
    except requests.RequestException:
        print("⚠️  Homelab service is not running (normal for development)")
    
    # Summary
    print("\n📊 Quick Test Summary")
    print("==================")
    
    if errors:
        print(f"❌ {len(errors)} error(s) found:")
        for error in errors:
            print(f"   • {error}")
        return False
    else:
        print("✅ All quick tests passed!")
        print("💡 Ready for development")
        return True

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
