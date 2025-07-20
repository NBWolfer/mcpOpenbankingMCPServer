"""
Market data and analysis tools
"""

import logging
from typing import Dict, Any, List
from agents.agent_manager import AgentManager


logger = logging.getLogger(__name__)


class MarketTools:
    """Tools for market data analysis"""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
    
    async def analyze_market(self, symbols: List[str], analysis_type: str = "general") -> str:
        """Analyze current market conditions"""
        try:
            context = f"Symbols: {symbols}\nAnalysis Type: {analysis_type}"
            
            prompt = f"""
            Please analyze the current market conditions for the specified symbols.
            
            Focus on:
            1. Current market trends and sentiment
            2. Technical indicators
            3. Fundamental factors affecting the market
            4. Volatility levels and patterns
            5. Market opportunities and risks
            6. Short-term and long-term outlook
            
            Provide actionable insights for investment decisions.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="market_analysis",
                context=context
            )
            
            return f"Market Analysis (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in market analysis: {e}")
            return f"Error analyzing market: {str(e)}"
    
    async def analyze_volatility(self, symbols: List[str], timeframe: str = "1d") -> str:
        """Analyze market volatility"""
        try:
            context = f"Symbols: {symbols}\nTimeframe: {timeframe}"
            
            prompt = f"""
            Please analyze the volatility characteristics for the specified symbols over the {timeframe} timeframe.
            
            Analyze:
            1. Historical volatility patterns
            2. Implied volatility (if applicable)
            3. Volatility clustering and mean reversion
            4. Volatility spillover effects
            5. Risk implications for portfolio management
            6. Volatility forecasting
            
            Identify periods of high volatility and their causes.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="market_analysis",
                context=context
            )
            
            return f"Volatility Analysis (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in volatility analysis: {e}")
            return f"Error analyzing volatility: {str(e)}"
    
    async def sector_analysis(self, sector: str) -> str:
        """Analyze specific sector performance and outlook"""
        try:
            context = f"Sector: {sector}"
            
            prompt = f"""
            Please provide a comprehensive analysis of the {sector} sector.
            
            Include:
            1. Current sector performance vs market
            2. Key drivers and headwinds
            3. Leading companies and their prospects
            4. Regulatory environment impact
            5. Technology and innovation trends
            6. Investment opportunities and risks
            7. Sector rotation considerations
            
            Provide both fundamental and technical perspectives.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="market_analysis",
                context=context
            )
            
            return f"Sector Analysis (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in sector analysis: {e}")
            return f"Error analyzing sector: {str(e)}"
    
    async def correlation_analysis(self, symbols: List[str]) -> str:
        """Analyze correlations between different assets"""
        try:
            context = f"Symbols for correlation analysis: {symbols}"
            
            prompt = f"""
            Please analyze the correlation structure between the provided assets.
            
            Examine:
            1. Pairwise correlations between assets
            2. Time-varying correlation patterns
            3. Correlation during different market regimes
            4. Diversification benefits analysis
            5. Risk concentration identification
            6. Correlation breakdown during stress periods
            
            Provide insights for portfolio construction and risk management.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="market_analysis",
                context=context
            )
            
            return f"Correlation Analysis (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in correlation analysis: {e}")
            return f"Error analyzing correlations: {str(e)}"
