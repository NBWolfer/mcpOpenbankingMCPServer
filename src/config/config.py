"""
Configuration management for the MCP OpenBanking Server
"""

import yaml
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class OllamaConfig:
    """Configuration for Ollama connection"""
    host: str = "localhost"
    port: int = 11434
    timeout: int = 30
    base_url: Optional[str] = None
    
    def __post_init__(self):
        if self.base_url is None:
            self.base_url = f"http://{self.host}:{self.port}"


@dataclass
class BankApiConfig:
    """Configuration for Bank API connection"""
    base_url: str = "http://localhost:3000"
    timeout: int = 10
    api_key: str = ""
    endpoints: Dict[str, str] = field(default_factory=lambda: {
        "customer": "/api/customers/{CustomerOID}",
        "portfolio": "/api/portfolio/{CustomerOID}",
        "transactions": "/api/transactions/{CustomerOID}",
        "accounts": "/api/accounts/{CustomerOID}",
        "market_data": "/api/market-data",
        "risk_metrics": "/api/risk/{CustomerOID}"
    })


@dataclass
class AgentConfig:
    """Configuration for individual agents"""
    name: str
    model: str
    role: str
    system_prompt: str
    temperature: float = 0.7
    max_tokens: int = 2048
    enabled: bool = True


@dataclass
class ToolConfig:
    """Configuration for tools"""
    name: str
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Config:
    """Main configuration class"""
    server_name: str = "openbanking-mcp"
    development_mode: bool = False
    ollama: OllamaConfig = field(default_factory=OllamaConfig)
    bank_api: BankApiConfig = field(default_factory=BankApiConfig)
    agents: List[AgentConfig] = field(default_factory=list)
    tools: List[ToolConfig] = field(default_factory=list)
    
    @classmethod
    def load(cls, config_path: str) -> 'Config':
        """Load configuration from YAML file"""
        config_file = Path(config_path)
        
        if not config_file.exists():
            # Create default config if it doesn't exist
            default_config = cls._create_default_config()
            default_config.save(config_path)
            return default_config
            
        with open(config_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        # Parse configuration
        config = cls()
        config.server_name = data.get('server_name', config.server_name)
        config.development_mode = data.get('development_mode', config.development_mode)
        
        # Parse Ollama config
        if 'ollama' in data:
            ollama_data = data['ollama']
            config.ollama = OllamaConfig(
                host=ollama_data.get('host', 'localhost'),
                port=ollama_data.get('port', 11434),
                timeout=ollama_data.get('timeout', 30)
            )
        
        # Parse Bank API config
        if 'bank_api' in data:
            bank_api_data = data['bank_api']
            config.bank_api = BankApiConfig(
                base_url=bank_api_data.get('base_url', 'http://localhost:3000'),
                timeout=bank_api_data.get('timeout', 10),
                api_key=bank_api_data.get('api_key', ''),
                endpoints=bank_api_data.get('endpoints', {})
            )
        
        # Parse agents
        if 'agents' in data:
            config.agents = [
                AgentConfig(**agent_data) 
                for agent_data in data['agents']
            ]
        
        # Parse tools
        if 'tools' in data:
            config.tools = [
                ToolConfig(**tool_data)
                for tool_data in data['tools']
            ]
            
        return config
    
    def save(self, config_path: str):
        """Save configuration to YAML file"""
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'server_name': self.server_name,
            'development_mode': self.development_mode,
            'ollama': {
                'host': self.ollama.host,
                'port': self.ollama.port,
                'timeout': self.ollama.timeout
            },
            'agents': [
                {
                    'name': agent.name,
                    'model': agent.model,
                    'role': agent.role,
                    'system_prompt': agent.system_prompt,
                    'temperature': agent.temperature,
                    'max_tokens': agent.max_tokens,
                    'enabled': agent.enabled
                }
                for agent in self.agents
            ],
            'tools': [
                {
                    'name': tool.name,
                    'enabled': tool.enabled,
                    'config': tool.config
                }
                for tool in self.tools
            ]
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, indent=2)
    
    @classmethod
    def _create_default_config(cls) -> 'Config':
        """Create default configuration"""
        config = cls()
        
        # Default agents based on the image
        config.agents = [
            AgentConfig(
                name="market_analyst",
                model="llama3.2:latest",
                role="Market Data Analyst", 
                system_prompt="You are a specialized market data analyst agent. Your role is to analyze market conditions, identify volatile situations, and provide insights on current market trends. Focus on real-time data analysis and market volatility assessment."
            ),
            AgentConfig(
                name="portfolio_manager",
                model="llama3.2:latest", 
                role="Portfolio Manager",
                system_prompt="You are a portfolio management agent specializing in strategy development. Your role is to analyze portfolios, recommend investment strategies, and provide optimization suggestions. Focus on risk-adjusted returns and strategic asset allocation."
            ),
            AgentConfig(
                name="risk_analyst", 
                model="llama3.2:latest",
                role="Risk Analyst",
                system_prompt="You are a risk analysis agent focused on user-specific risk assessment. Your role is to evaluate financial risks, assess user risk profiles, and provide risk management recommendations. Focus on personalized risk analysis and mitigation strategies."
            ),
            AgentConfig(
                name="explainability_agent",
                model="llama3.2:latest",
                role="Explainability & Strategy Agent", 
                system_prompt="You are an explainability agent specializing in making complex financial concepts understandable. Your role is to provide clear explanations, conduct SWOT analysis, and help users understand financial decisions. Focus on clarity and educational value."
            )
        ]
        
        # Default tools
        config.tools = [
            ToolConfig(name="portfolio_analysis", enabled=True),
            ToolConfig(name="market_data", enabled=True),
            ToolConfig(name="risk_assessment", enabled=True),
            ToolConfig(name="strategy_recommendation", enabled=True),
            ToolConfig(name="swot_analysis", enabled=True),
            ToolConfig(name="reverse_simulation", enabled=True)
        ]
        
        return config
