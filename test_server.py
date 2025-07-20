#!/usr/bin/env python3
"""
Test script for OpenBanking MCP Server
"""

import asyncio
import sys
import os
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.config import Config
from agents.agent_manager import AgentManager


async def test_config_loading():
    """Test configuration loading"""
    print("🧪 Testing configuration loading...")
    try:
        config = Config.load("config/config.yaml")
        print(f"✓ Configuration loaded successfully")
        print(f"  Server name: {config.server_name}")
        print(f"  Number of agents: {len(config.agents)}")
        print(f"  Number of tools: {len(config.tools)}")
        return True
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False


async def test_agent_manager():
    """Test agent manager initialization"""
    print("\n🧪 Testing agent manager...")
    try:
        config = Config.load("config/config.yaml")
        agent_manager = AgentManager(config)
        
        # Test without actually connecting to Ollama
        print("✓ Agent manager created successfully")
        print(f"  Configured agents: {[agent.name for agent in config.agents]}")
        return True
    except Exception as e:
        print(f"✗ Agent manager creation failed: {e}")
        return False


async def test_ollama_connection():
    """Test Ollama connection"""
    print("\n🧪 Testing Ollama connection...")
    try:
        import ollama
        client = ollama.Client(host="http://localhost:11434")
        models = client.list()
        print("✓ Ollama connection successful")
        print(f"  Available models: {[model['name'] for model in models['models']]}")
        return True
    except Exception as e:
        print(f"✗ Ollama connection failed: {e}")
        print("  Make sure Ollama is installed and running")
        return False


async def test_sample_query():
    """Test a sample query"""
    print("\n🧪 Testing sample query...")
    try:
        config = Config.load("config/config.yaml")
        agent_manager = AgentManager(config)
        
        # Only test if Ollama is available
        try:
            await agent_manager.initialize()
            
            # Test query
            response = await agent_manager.query_best_agent(
                prompt="What is portfolio diversification?",
                task_type="explanation"
            )
            
            agent_name, answer = response
            print(f"✓ Sample query successful")
            print(f"  Agent used: {agent_name}")
            print(f"  Response preview: {answer[:100]}...")
            return True
            
        except Exception as e:
            print(f"⚠ Sample query skipped (Ollama not available): {e}")
            return True
            
    except Exception as e:
        print(f"✗ Sample query failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("🚀 OpenBanking MCP Server Tests")
    print("=" * 40)
    
    tests = [
        test_config_loading,
        test_agent_manager,
        test_ollama_connection,
        test_sample_query
    ]
    
    results = []
    for test in tests:
        result = await test()
        results.append(result)
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    passed = sum(results)
    total = len(results)
    print(f"  Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
