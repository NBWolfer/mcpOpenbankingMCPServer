#!/usr/bin/env python3
"""
Quick test to check Ollama models and connection
"""

import asyncio
import sys

async def test_ollama():
    try:
        # Install ollama if needed
        try:
            import ollama
        except ImportError:
            print("Installing ollama package...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ollama"])
            import ollama
        
        print("🔍 Testing Ollama connection...")
        
        # Test connection
        client = ollama.Client(host="http://localhost:11434")
        
        # List models
        models_response = await asyncio.to_thread(client.list)
        models = models_response['models']
        
        print("✅ Ollama connection successful!")
        print(f"📋 Available models ({len(models)}):")
        
        for model in models:
            name = model['name']
            size = model.get('size', 0)
            size_gb = size / (1024**3) if size > 0 else 0
            print(f"  • {name} ({size_gb:.1f}GB)")
        
        # Test a simple query with the first available model
        if models:
            test_model = models[0]['name']
            print(f"\n🧪 Testing query with model: {test_model}")
            
            try:
                response = await asyncio.to_thread(
                    client.generate,
                    model=test_model,
                    prompt="Hello, can you explain what portfolio diversification means in one sentence?",
                    options={'num_predict': 50}
                )
                
                print("✅ Query test successful!")
                print(f"📝 Response: {response['response']}")
                
                return test_model
                
            except Exception as e:
                print(f"❌ Query test failed: {e}")
                return None
        else:
            print("❌ No models available")
            return None
            
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        return None

async def main():
    print("🚀 Ollama Test Script")
    print("=" * 30)
    
    model = await test_ollama()
    
    if model:
        print(f"\n✅ Success! You can use model: {model}")
        print(f"💡 Update your config.yaml to use this model name")
    else:
        print(f"\n❌ No working models found")
        print(f"💡 Try: ollama pull gemma2:2b")

if __name__ == "__main__":
    asyncio.run(main())
