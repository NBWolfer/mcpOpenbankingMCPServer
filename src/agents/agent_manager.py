"""
Agent Manager for handling multiple LLM agents
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
import ollama

from config.config import Config, AgentConfig
from utils.bank_api_client import BankApiClient


logger = logging.getLogger(__name__)


class Agent:
    """Individual agent wrapper for Ollama models"""
    
    def __init__(self, config: AgentConfig, ollama_client, bank_api_client: BankApiClient):
        self.config = config
        self.client = ollama_client
        self.bank_api_client = bank_api_client
        self.name = config.name
        self.model = config.model
        self.model_name = config.model
        self.role = config.role
        self.is_available = False
        
    async def generate_response(
        self, 
        prompt: str, 
        context: Optional[str] = None,
        customer_oid: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate response using the agent's model with optional customer data"""
        try:
            # Construct the full prompt with system prompt and context
            full_prompt = self.config.system_prompt + "\n\n"
            
            # Fetch customer data if CustomerOID is provided
            if customer_oid:
                logger.info(f"Fetching customer data for {customer_oid}")
                customer_data = await self.bank_api_client.get_comprehensive_customer_data(customer_oid)
                
                # Add customer data to context
                customer_context = f"""
Customer Data for {customer_oid}:
- Customer Profile: {customer_data.get('customer', {})}
- Portfolio: {customer_data.get('portfolio', {})}
- Accounts: {customer_data.get('accounts', {})}
- Recent Transactions: {customer_data.get('transactions', {})}
- Risk Metrics: {customer_data.get('risk_metrics', {})}
"""
                
                if context:
                    full_prompt += f"Context: {context}\n\n"
                full_prompt += f"Customer Context: {customer_context}\n\n"
            elif context:
                full_prompt += f"Context: {context}\n\n"
                
            full_prompt += f"User Query: {prompt}"
            
            # Generate response using Ollama
            response = await asyncio.to_thread(
                self.client.generate,
                model=self.model,
                prompt=full_prompt,
                options={
                    'temperature': kwargs.get('temperature', self.config.temperature),
                    'num_predict': kwargs.get('max_tokens', self.config.max_tokens)
                }
            )
            
            return response['response']
            
        except Exception as e:
            logger.error(f"Error generating response with agent {self.name}: {e}")
            return f"Error: Unable to generate response - {str(e)}"
    
    async def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool using this agent's capabilities"""
        try:
            customer_oid = arguments.get("customer_oid") or arguments.get("CustomerOID")
            
            # Create a prompt for tool execution
            prompt = f"""
Execute the following tool: {tool_name}
Arguments: {arguments}

Please provide a detailed response based on your role as {self.role}.
Analyze the request and provide insights according to your expertise.
If customer data is available, provide personalized recommendations.
"""
            
            response = await self.generate_response(prompt, customer_oid=customer_oid)
            return response
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name} with agent {self.name}: {e}")
            return f"Error: Unable to execute tool - {str(e)}"
    
    async def is_model_available(self) -> bool:
        """Check if the model is available in Ollama"""
        try:
            models_response = await asyncio.to_thread(self.client.list)
            
            # Handle different response formats
            available_models = []
            
            if hasattr(models_response, 'models'):
                # If it's an object with models attribute
                models_list = models_response.models
            elif isinstance(models_response, dict) and 'models' in models_response:
                # If it's a dict with models key
                models_list = models_response['models']
            elif isinstance(models_response, list):
                # If it's directly a list
                models_list = models_response
            else:
                logger.error(f"Unexpected models response format: {models_response}")
                return False
            
            # Extract model names from different possible formats
            for model in models_list:
                if hasattr(model, 'model'):
                    # Model object with model attribute
                    available_models.append(model.model)
                elif isinstance(model, dict):
                    # Dictionary format
                    name = model.get('name') or model.get('model', '')
                    if name:
                        available_models.append(name)
                elif isinstance(model, str):
                    # String format
                    available_models.append(model)
            
            # Remove empty strings
            available_models = [m for m in available_models if m]
            
            logger.info(f"Available models: {available_models}")
            
            # Check exact match first
            if self.model in available_models:
                return True
            
            # Check if model exists with different tag
            model_base = self.model.split(':')[0]
            for available_model in available_models:
                if available_model.startswith(model_base):
                    logger.info(f"Using available model {available_model} instead of {self.model}")
                    self.model = available_model  # Update to use the available model
                    return True
            
            logger.warning(f"Model {self.model} not found in available models: {available_models}")
            return False
            
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False


class AgentManager:
    """Manager for all agents"""
    
    def __init__(self, config: Config):
        self.config = config
        self.agents: Dict[str, Agent] = {}
        self.ollama_client = None
        self.bank_api_client = BankApiClient(config.bank_api)
        
    async def initialize(self):
        """Initialize the agent manager and all agents"""
        try:
            # Initialize Ollama client
            self.ollama_client = ollama.Client(
                host=self.config.ollama.base_url
            )
            
            # Test connection
            await self._test_ollama_connection()
            
            # Initialize agents
            await self._initialize_agents()
            
            logger.info(f"AgentManager initialized with {len(self.agents)} agents")
            
        except Exception as e:
            logger.error(f"Failed to initialize AgentManager: {e}")
            raise
    
    async def _test_ollama_connection(self):
        """Test connection to Ollama server"""
        try:
            await asyncio.to_thread(self.ollama_client.list)
            logger.info("Successfully connected to Ollama server")
        except Exception as e:
            logger.error(f"Failed to connect to Ollama server: {e}")
            raise
    
    async def _initialize_agents(self):
        """Initialize all configured agents"""
        for agent_config in self.config.agents:
            if not agent_config.enabled:
                continue
                
            try:
                agent = Agent(agent_config, self.ollama_client, self.bank_api_client)
                
                # Check if model is available
                if await agent.is_model_available():
                    agent.is_available = True
                    self.agents[agent_config.name] = agent
                    logger.info(f"Initialized agent: {agent_config.name} with model: {agent_config.model}")
                else:
                    logger.warning(f"Model {agent_config.model} not available for agent {agent_config.name}")
                    
            except Exception as e:
                logger.error(f"Failed to initialize agent {agent_config.name}: {e}")
    
    def get_agent(self, agent_name: str) -> Optional[Agent]:
        """Get agent by name"""
        return self.agents.get(agent_name)
    
    def list_agents(self) -> List[str]:
        """List all available agent names"""
        return list(self.agents.keys())
    
    async def query_agent(
        self, 
        agent_name: str, 
        prompt: str, 
        context: Optional[str] = None,
        **kwargs
    ) -> str:
        """Query a specific agent"""
        agent = self.get_agent(agent_name)
        if not agent:
            return f"Error: Agent '{agent_name}' not found"
            
        return await agent.generate_response(prompt, context, **kwargs)
    
    async def query_best_agent(
        self, 
        prompt: str, 
        task_type: str = "general",
        context: Optional[str] = None,
        **kwargs
    ) -> tuple[str, str]:
        """Query the best agent for a specific task type"""
        
        # Define agent selection based on task type
        task_agent_mapping = {
            "market_analysis": "market_analyst",
            "portfolio": "portfolio_manager", 
            "risk": "risk_analyst",
            "explanation": "explainability_agent",
            "swot": "explainability_agent",
            "strategy": "portfolio_manager",
            "general": "explainability_agent"
        }
        
        preferred_agent = task_agent_mapping.get(task_type, "explainability_agent")
        
        # Try preferred agent first
        if preferred_agent in self.agents:
            response = await self.query_agent(preferred_agent, prompt, context, **kwargs)
            return preferred_agent, response
        
        # Fallback to any available agent
        if self.agents:
            fallback_agent = list(self.agents.keys())[0]
            response = await self.query_agent(fallback_agent, prompt, context, **kwargs)
            return fallback_agent, response
        
        return "none", "Error: No agents available"
    
    async def shutdown(self):
        """Shutdown the agent manager"""
        logger.info("Shutting down AgentManager")
        self.agents.clear()
    
    def get_agent_for_tool(self, tool_name: str) -> Optional[Agent]:
        """Get the appropriate agent for a specific tool"""
        # Define tool-to-agent mappings
        tool_agent_mapping = {
            # Market analysis tools
            "get_market_data": "market_analyst",
            "analyze_stock": "market_analyst", 
            "get_economic_indicators": "market_analyst",
            "market_sentiment": "market_analyst",
            
            # Portfolio tools
            "portfolio_analysis": "portfolio_manager",
            "asset_allocation": "portfolio_manager",
            "rebalance_portfolio": "portfolio_manager",
            "performance_metrics": "portfolio_manager",
            
            # Risk tools
            "calculate_var": "risk_analyst",
            "stress_test": "risk_analyst",
            "correlation_analysis": "risk_analyst",
            "risk_metrics": "risk_analyst",
            
            # Strategy tools
            "backtest_strategy": "portfolio_manager",
            "optimize_portfolio": "portfolio_manager",
            "generate_signals": "market_analyst",
            
            # Explanation tools
            "explain_analysis": "explainability_agent",
            "swot_analysis": "explainability_agent",
            "summarize_results": "explainability_agent"
        }
        
        agent_name = tool_agent_mapping.get(tool_name)
        return self.get_agent(agent_name) if agent_name else None

    @property
    def is_available(self) -> bool:
        """Check if any agents are available"""
        return len(self.agents) > 0
