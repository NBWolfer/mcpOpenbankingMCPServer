#!/usr/bin/env python3
"""
Startup script for OpenBanking MCP Server
"""

import sys
import os
import subprocess
import argparse

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import ollama
        import yaml
        import pydantic
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def check_ollama_server():
    """Check if Ollama server is running"""
    try:
        import ollama
        client = ollama.Client()
        client.list()
        print("✓ Ollama server is running")
        return True
    except Exception as e:
        print(f"✗ Ollama server is not accessible: {e}")
        print("Please make sure Ollama is installed and running")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✓ Dependencies installed")

def main():
    parser = argparse.ArgumentParser(description="OpenBanking MCP Server Startup")
    parser.add_argument("--install", action="store_true", help="Install dependencies first")
    parser.add_argument("--dev", action="store_true", help="Run in development mode")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("🚀 OpenBanking MCP Server Startup")
    print("=" * 40)
    
    # Install dependencies if requested
    if args.install:
        install_dependencies()
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install dependencies first:")
        print("python startup.py --install")
        return 1
    
    # Check Ollama server
    if not check_ollama_server():
        return 1
    
    # Start the server
    print("\n🎯 Starting MCP Server...")
    
    cmd = [sys.executable, "src/main.py"]
    if args.dev:
        cmd.append("--dev")
    if args.config != "config/config.yaml":
        cmd.extend(["--config", args.config])
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed with exit code {e.returncode}")
        return e.returncode
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
