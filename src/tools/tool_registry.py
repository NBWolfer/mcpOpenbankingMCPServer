"""
Tool Registry for MCP Server
Manages and registers all available tools
"""

import logging
from typing import Dict, Any, List
from mcp.server import Server
from mcp.types import Tool, TextContent

from agents.agent_manager import AgentManager
from tools.portfolio_tools import PortfolioTools
from tools.market_tools import MarketTools
from tools.risk_tools import RiskTools
from tools.strategy_tools import StrategyTools
from tools.analysis_tools import AnalysisTools


logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry for managing all MCP tools"""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
        self.tools: Dict[str, Any] = {}
        self.registered_tools: Dict[str, str] = {}  # Track registered tools
        
        # Initialize tool modules
        self.portfolio_tools = PortfolioTools(agent_manager)
        self.market_tools = MarketTools(agent_manager)
        self.risk_tools = RiskTools(agent_manager)
        self.strategy_tools = StrategyTools(agent_manager)
        self.analysis_tools = AnalysisTools(agent_manager)
    
    async def register_tools(self, server: Server):
        """Register all tools with the MCP server"""
        
        # Portfolio Analysis Tools
        await self._register_portfolio_tools(server)
        
        # Market Data Tools
        await self._register_market_tools(server)
        
        # Risk Assessment Tools
        await self._register_risk_tools(server)
        
        # Strategy Tools
        await self._register_strategy_tools(server)
        
        # Analysis Tools
        await self._register_analysis_tools(server)
        
        logger.info(f"Registered {len(self.registered_tools)} tools with MCP server")
        
    def _track_tool(self, tool_name: str, description: str):
        """Track a registered tool"""
        self.registered_tools[tool_name] = description
    
    async def _register_portfolio_tools(self, server: Server):
        """Register portfolio analysis tools"""
        
        @server.call_tool()
        async def analyze_portfolio(arguments: dict) -> List[TextContent]:
            """Analyze portfolio performance and composition"""
            portfolio_data = arguments.get("portfolio_data", {})
            analysis_type = arguments.get("analysis_type", "comprehensive")
            
            result = await self.portfolio_tools.analyze_portfolio(portfolio_data, analysis_type)
            return [TextContent(type="text", text=result)]
        
        @server.call_tool()
        async def portfolio_optimization(arguments: dict) -> List[TextContent]:
            """Optimize portfolio allocation"""
            portfolio_data = arguments.get("portfolio_data", {})
            optimization_method = arguments.get("method", "mean_variance")
            constraints = arguments.get("constraints", {})
            
            result = await self.portfolio_tools.optimize_portfolio(
                portfolio_data, optimization_method, constraints
            )
            return [TextContent(type="text", text=result)]
        
        # Track registered tools
        self._track_tool("analyze_portfolio", "Analyze portfolio performance and composition")
        self._track_tool("portfolio_optimization", "Optimize portfolio allocation")
        
        # Register tool definitions
        server.list_tools = lambda: [
            Tool(
                name="analyze_portfolio",
                description="Analyze portfolio performance, composition, and provide insights",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "portfolio_data": {
                            "type": "object",
                            "description": "Portfolio data including holdings, weights, and performance metrics"
                        },
                        "analysis_type": {
                            "type": "string",
                            "enum": ["comprehensive", "performance", "risk", "composition"],
                            "description": "Type of analysis to perform"
                        }
                    },
                    "required": ["portfolio_data"]
                }
            ),
            Tool(
                name="portfolio_optimization",
                description="Optimize portfolio allocation based on various methods",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "portfolio_data": {
                            "type": "object",
                            "description": "Current portfolio data"
                        },
                        "method": {
                            "type": "string",
                            "enum": ["mean_variance", "risk_parity", "max_diversification"],
                            "description": "Optimization method to use"
                        },
                        "constraints": {
                            "type": "object",
                            "description": "Investment constraints (min/max weights, sectors, etc.)"
                        }
                    },
                    "required": ["portfolio_data"]
                }
            )
        ]
    
    async def _register_market_tools(self, server: Server):
        """Register market data and analysis tools"""
        
        @server.call_tool()
        async def market_analysis(arguments: dict) -> List[TextContent]:
            """Analyze current market conditions"""
            symbols = arguments.get("symbols", [])
            analysis_type = arguments.get("analysis_type", "general")
            
            result = await self.market_tools.analyze_market(symbols, analysis_type)
            return [TextContent(type="text", text=result)]
        
        @server.call_tool()
        async def volatility_analysis(arguments: dict) -> List[TextContent]:
            """Analyze market volatility"""
            symbols = arguments.get("symbols", [])
            timeframe = arguments.get("timeframe", "1d")
            
            result = await self.market_tools.analyze_volatility(symbols, timeframe)
            return [TextContent(type="text", text=result)]
    
    async def _register_risk_tools(self, server: Server):
        """Register risk assessment tools"""
        
        @server.call_tool()
        async def assess_risk(arguments: dict) -> List[TextContent]:
            """Assess risk for user portfolio or investment"""
            portfolio_data = arguments.get("portfolio_data", {})
            user_profile = arguments.get("user_profile", {})
            risk_type = arguments.get("risk_type", "comprehensive")
            
            result = await self.risk_tools.assess_risk(portfolio_data, user_profile, risk_type)
            return [TextContent(type="text", text=result)]
        
        @server.call_tool()
        async def risk_simulation(arguments: dict) -> List[TextContent]:
            """Run risk simulation scenarios"""
            portfolio_data = arguments.get("portfolio_data", {})
            scenarios = arguments.get("scenarios", [])
            
            result = await self.risk_tools.simulate_scenarios(portfolio_data, scenarios)
            return [TextContent(type="text", text=result)]
    
    async def _register_strategy_tools(self, server: Server):
        """Register strategy recommendation tools"""
        
        @server.call_tool()
        async def recommend_strategy(arguments: dict) -> List[TextContent]:
            """Recommend investment strategy"""
            user_profile = arguments.get("user_profile", {})
            market_conditions = arguments.get("market_conditions", {})
            strategy_type = arguments.get("strategy_type", "balanced")
            
            result = await self.strategy_tools.recommend_strategy(
                user_profile, market_conditions, strategy_type
            )
            return [TextContent(type="text", text=result)]
    
    async def _register_analysis_tools(self, server: Server):
        """Register analysis and explainability tools"""
        
        @server.call_tool()
        async def swot_analysis(arguments: dict) -> List[TextContent]:
            """Perform SWOT analysis"""
            subject = arguments.get("subject", "")
            context = arguments.get("context", {})
            
            result = await self.analysis_tools.swot_analysis(subject, context)
            return [TextContent(type="text", text=result)]
        
        @server.call_tool()
        async def explain_concept(arguments: dict) -> List[TextContent]:
            """Explain financial concepts in simple terms"""
            concept = arguments.get("concept", "")
            complexity_level = arguments.get("complexity_level", "intermediate")
            
            result = await self.analysis_tools.explain_concept(concept, complexity_level)
            return [TextContent(type="text", text=result)]
        
        @server.call_tool()
        async def reverse_simulation(arguments: dict) -> List[TextContent]:
            """Perform reverse simulation analysis"""
            target_outcome = arguments.get("target_outcome", {})
            current_state = arguments.get("current_state", {})
            
            result = await self.analysis_tools.reverse_simulation(target_outcome, current_state)
            return [TextContent(type="text", text=result)]
