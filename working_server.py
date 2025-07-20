#!/usr/bin/env python3
"""
Working MCP Server with direct Ollama subprocess calls
"""

import asyncio
import logging
import sys
import os
import subprocess
import json
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DirectOllamaAgent:
    """Agent that calls Ollama directly via subprocess"""
    
    def __init__(self, name: str, model: str, role: str, system_prompt: str):
        self.name = name
        self.model = model
        self.role = role
        self.system_prompt = system_prompt
    
    async def generate_response(self, prompt: str, context: str = None) -> str:
        """Generate response using direct Ollama subprocess call"""
        try:
            # Construct the full prompt
            full_prompt = f"{self.system_prompt}\n\n"
            
            if context:
                full_prompt += f"Context: {context}\n\n"
                
            full_prompt += f"User Query: {prompt}\n\nResponse:"
            
            # Call Ollama directly
            cmd = ['ollama', 'run', self.model, full_prompt]
            
            # Run the command
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                response = stdout.decode('utf-8').strip()
                return response
            else:
                error_msg = stderr.decode('utf-8').strip()
                logger.error(f"Ollama error: {error_msg}")
                return f"Error: {error_msg}"
                
        except Exception as e:
            logger.error(f"Error calling Ollama: {e}")
            return f"Error calling Ollama: {str(e)}"


class WorkingMCPServer:
    """Working MCP Server with direct Ollama calls"""
    
    def __init__(self):
        self.agents = {}
        self.initialize_agents()
    
    def initialize_agents(self):
        """Initialize agents with direct Ollama calls"""
        
        # Agent configurations (using your available model: gemma3:4b with updated prompts)
        agent_configs = [
            {
                "name": "market_analyst",
                "model": "gemma3:4b",
                "role": "Market Data Analyst",
                "system_prompt": "You are a specialized market data analyst agent. Your primary role is to evaluate the market context in relation to the portfolio strategies proposed by the portfolio_manager agent. Focus on identifying current market trends, volatility indicators, and how these conditions may impact the proposed asset allocations or adjustments. Consider cross-asset relationships, macroeconomic signals, and market sentiment. Your goal is to determine which market conditions favor or challenge the recommended strategies."
            },
            {
                "name": "portfolio_manager", 
                "model": "gemma3:4b",
                "role": "Portfolio Manager",
                "system_prompt": "You are a portfolio management agent responsible for assessing user portfolios and designing optimal investment strategies. Evaluate current portfolio allocation, diversification quality, and exposure to risk factors. Propose asset allocation adjustments or strategy changes to optimize for risk-adjusted returns. Provide context-aware suggestions that will later be assessed for market compatibility by the Market Data Analyst Agent."
            },
            {
                "name": "risk_analyst",
                "model": "gemma3:4b", 
                "role": "Risk Analyst",
                "system_prompt": "You are a financial risk analysis agent specializing in options-based strategies. Your role is to assess the user's portfolio and market conditions to propose options strategies (e.g. protective puts, covered calls, spreads) for hedging or leveraged exposure. Evaluate the risk profile of the user and recommend tailored strategies for risk mitigation or opportunity leveraging. Coordinate with insights from Market Data Analyst Agent and Portfolio Manager Agent when available."
            },
            {
                "name": "explainability_agent",
                "model": "gemma3:4b",
                "role": "Explainability Agent", 
                "system_prompt": "You are a financial explainability agent specialized in making strategic financial concepts transparent and easy to understand. Your tasks include reverse simulation of strategies, interpreting options structures, explaining portfolio management decisions, and answering user questions in simple terms. Present information in an educational and conversational style, acting as an intelligent assistant. Provide strategic clarity and reasoning behind decisions proposed by other agents."
            }
        ]
        
        # Create agents
        for config in agent_configs:
            agent = DirectOllamaAgent(
                name=config["name"],
                model=config["model"],
                role=config["role"],
                system_prompt=config["system_prompt"]
            )
            self.agents[config["name"]] = agent
            
        logger.info(f"Initialized {len(self.agents)} agents")
    
    def get_best_agent_for_task(self, task_type: str) -> str:
        """Get the best agent for a specific task type"""
        task_mapping = {
            "market": "market_analyst",
            "portfolio": "portfolio_manager", 
            "risk": "risk_analyst",
            "explanation": "explainability_agent",
            "swot": "explainability_agent",
            "general": "explainability_agent"
        }
        
        return task_mapping.get(task_type, "explainability_agent")
    
    async def query_agent(self, agent_name: str, prompt: str, context: str = None) -> str:
        """Query a specific agent"""
        if agent_name not in self.agents:
            return f"Error: Agent '{agent_name}' not found"
        
        agent = self.agents[agent_name]
        return await agent.generate_response(prompt, context)
    
    async def query_best_agent(self, prompt: str, task_type: str = "general", context: str = None) -> tuple[str, str]:
        """Query the best agent for a task"""
        agent_name = self.get_best_agent_for_task(task_type)
        response = await self.query_agent(agent_name, prompt, context)
        return agent_name, response
    
    async def test_connection(self) -> bool:
        """Test if Ollama is working"""
        try:
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except:
            return False
    
    async def run_interactive(self):
        """Run interactive mode"""
        print("\n🚀 OpenBanking MCP Server - Interactive Mode")
        print("Available commands:")
        print("  help - Show commands")
        print("  agents - List agents")
        print("  quit - Exit")
        print("  Any other text - Query the agents")
        print("-" * 50)
        
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
                    print("  market:<query> - Ask market analyst")
                    print("  portfolio:<query> - Ask portfolio manager")
                    print("  risk:<query> - Ask risk analyst")
                    print("  explain:<query> - Ask explanation agent")
                    print("  Any other text - Auto-select best agent")
                    continue
                elif user_input.lower() == 'agents':
                    print(f"\nAvailable agents:")
                    for name, agent in self.agents.items():
                        print(f"  • {name} ({agent.role})")
                    continue
                elif not user_input:
                    continue
                
                # Parse task-specific queries
                if ':' in user_input:
                    task_type, query = user_input.split(':', 1)
                    task_type = task_type.strip().lower()
                    query = query.strip()
                else:
                    # Auto-detect task type
                    task_type = "general"
                    query = user_input
                    
                    # Simple keyword detection
                    if any(word in query.lower() for word in ['market', 'price', 'volatility', 'trend']):
                        task_type = "market"
                    elif any(word in query.lower() for word in ['portfolio', 'allocation', 'invest']):
                        task_type = "portfolio"
                    elif any(word in query.lower() for word in ['risk', 'danger', 'safe']):
                        task_type = "risk"
                    elif any(word in query.lower() for word in ['explain', 'what is', 'how does']):
                        task_type = "explanation"
                
                print(f"\n🤖 Processing with {task_type} agent...")
                
                agent_name, response = await self.query_best_agent(query, task_type)
                
                print(f"\n📋 Response from {agent_name}:")
                print("=" * 50)
                print(response)
                print("=" * 50)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        print("\n👋 Goodbye!")


async def main():
    """Main function"""
    print("🚀 OpenBanking MCP Server - Working Version with gemma3:4b")
    print("=" * 60)
    
    server = WorkingMCPServer()
    
    # Test Ollama connection
    if not await server.test_connection():
        print("❌ Ollama is not running or not accessible")
        print("💡 Please start Ollama: ollama serve")
        return 1
    
    print("✅ Ollama connection successful")
    print(f"✅ Initialized {len(server.agents)} agents using gemma3:4b model")
    
    # Run a quick test
    print("\n🧪 Testing agent communication...")
    try:
        agent_name, response = await server.query_best_agent(
            "What is portfolio diversification?", 
            "explanation"
        )
        print(f"✅ Test successful! {agent_name} responded.")
        print(f"📝 Sample response: {response[:100]}...")
    except Exception as e:
        print(f"⚠ Test failed: {e}")
    
    # Start interactive mode
    await server.run_interactive()
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
