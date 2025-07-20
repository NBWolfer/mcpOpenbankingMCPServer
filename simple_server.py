#!/usr/bin/env python3
"""
Simplified MCP OpenBanking Server for testing
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    from config.config import Config
    from agents.agent_manager import AgentManager
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all dependencies are installed and you're in the correct directory")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimpleMCPServer:
    """Simplified MCP Server for testing"""
    
    def __init__(self):
        self.config = None
        self.agent_manager = None
    
    async def initialize(self):
        """Initialize the server"""
        try:
            # Load configuration
            config_path = current_dir / "config" / "config.yaml"
            if not config_path.exists():
                logger.error(f"Configuration file not found: {config_path}")
                return False
                
            self.config = Config.load(str(config_path))
            logger.info("Configuration loaded successfully")
            
            # Initialize agent manager
            self.agent_manager = AgentManager(self.config)
            
            # Try to initialize agents (will fail gracefully if Ollama is not available)
            try:
                await self.agent_manager.initialize()
                logger.info("Agent manager initialized successfully")
            except Exception as e:
                logger.warning(f"Agent manager initialization failed (Ollama not available?): {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize server: {e}")
            return False
    
    async def test_query(self):
        """Test a simple query"""
        if not self.agent_manager or not self.agent_manager.agents:
            logger.warning("No agents available for testing")
            return
        
        try:
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt="Explain what portfolio diversification means in simple terms.",
                task_type="explanation"
            )
            
            print(f"\n🤖 Response from {agent_name}:")
            print("=" * 50)
            print(response)
            print("=" * 50)
            
        except Exception as e:
            logger.error(f"Error in test query: {e}")
    
    async def run_interactive(self):
        """Run interactive mode"""
        print("\n🚀 Interactive MCP Server Mode")
        print("Type 'quit' to exit, 'help' for commands")
        print("-" * 40)
        
        while True:
            try:
                user_input = input("\n💬 Enter your query: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                elif user_input.lower() == 'help':
                    print("\nAvailable commands:")
                    print("  help - Show this help")
                    print("  agents - List available agents")
                    print("  quit - Exit the server")
                    print("  Any other text - Query the agents")
                    continue
                elif user_input.lower() == 'agents':
                    if self.agent_manager:
                        agents = self.agent_manager.list_agents()
                        print(f"\nAvailable agents: {agents}")
                    else:
                        print("\nNo agent manager available")
                    continue
                elif not user_input:
                    continue
                
                if self.agent_manager and self.agent_manager.agents:
                    agent_name, response = await self.agent_manager.query_best_agent(
                        prompt=user_input,
                        task_type="general"
                    )
                    
                    print(f"\n🤖 {agent_name}:")
                    print(response)
                else:
                    print("\n⚠ No agents available. Check Ollama connection and configuration.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        print("\n👋 Goodbye!")


async def main():
    """Main function"""
    print("🚀 OpenBanking MCP Server - Simple Mode")
    print("=" * 50)
    
    server = SimpleMCPServer()
    
    # Initialize server
    if not await server.initialize():
        print("❌ Failed to initialize server")
        return 1
    
    print("✅ Server initialized successfully")
    
    # Run test query
    await server.test_query()
    
    # Start interactive mode
    await server.run_interactive()
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
