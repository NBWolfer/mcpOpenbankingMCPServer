#!/usr/bin/env python3
"""
Direct test script without complex imports
"""

import subprocess
import json

def test_ollama_direct():
    """Test Ollama directly via command line"""
    print("🔍 Testing Ollama via command line...")
    
    try:
        # Check if ollama is available
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        
        if result.returncode == 0:
            print("✅ Ollama is running!")
            print("📋 Available models:")
            print(result.stdout)
            
            # Test a simple generation
            print("\n🧪 Testing model generation...")
            test_result = subprocess.run([
                'ollama', 'run', 'gemma2:2b', 
                'Say hello in one sentence'
            ], capture_output=True, text=True, timeout=30)
            
            if test_result.returncode == 0:
                print("✅ Model generation successful!")
                print(f"📝 Response: {test_result.stdout.strip()}")
                return True
            else:
                print(f"❌ Model generation failed: {test_result.stderr}")
                return False
        else:
            print(f"❌ Ollama not running or error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Ollama command not found. Is Ollama installed?")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Ollama command timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Simple Ollama Test")
    print("=" * 30)
    
    if test_ollama_direct():
        print("\n✅ Ollama is working correctly!")
        print("💡 The issue might be in the Python integration")
    else:
        print("\n❌ Ollama is not working")
        print("💡 Try: ollama serve")
        print("💡 Then: ollama pull gemma2:2b")
