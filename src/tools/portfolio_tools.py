"""
Portfolio analysis tools
"""

import logging
from typing import Dict, Any, List
from agents.agent_manager import AgentManager


logger = logging.getLogger(__name__)


class PortfolioTools:
    """Tools for portfolio analysis and optimization"""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
    
    async def analyze_portfolio(self, portfolio_data: Dict[str, Any], analysis_type: str = "comprehensive") -> str:
        """Analyze portfolio performance and composition"""
        try:
            # Prepare context for the agent
            context = f"Portfolio Data: {portfolio_data}\nAnalysis Type: {analysis_type}"
            
            prompt = f"""
            Please analyze the provided portfolio data. Focus on:
            
            1. Asset allocation and diversification
            2. Performance metrics (returns, volatility, Sharpe ratio)
            3. Risk assessment
            4. Sector and geographic exposure
            5. Recommendations for improvement
            
            Provide a comprehensive analysis with specific insights and actionable recommendations.
            """
            
            # Use portfolio manager agent for this analysis
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="portfolio",
                context=context
            )
            
            return f"Portfolio Analysis (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in portfolio analysis: {e}")
            return f"Error analyzing portfolio: {str(e)}"
    
    async def optimize_portfolio(
        self, 
        portfolio_data: Dict[str, Any], 
        method: str = "mean_variance",
        constraints: Dict[str, Any] = None
    ) -> str:
        """Optimize portfolio allocation"""
        try:
            if constraints is None:
                constraints = {}
                
            context = f"""
            Portfolio Data: {portfolio_data}
            Optimization Method: {method}
            Constraints: {constraints}
            """
            
            prompt = f"""
            Please provide portfolio optimization recommendations using the {method} method.
            
            Consider:
            1. Current portfolio composition
            2. Expected returns and risk characteristics
            3. Correlation between assets
            4. Any specified constraints
            5. Optimal weight allocation
            
            Provide specific weight recommendations and explain the rationale behind the optimization.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="portfolio",
                context=context
            )
            
            return f"Portfolio Optimization (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in portfolio optimization: {e}")
            return f"Error optimizing portfolio: {str(e)}"
    
    async def performance_attribution(self, portfolio_data: Dict[str, Any], benchmark_data: Dict[str, Any]) -> str:
        """Analyze portfolio performance attribution"""
        try:
            context = f"""
            Portfolio Data: {portfolio_data}
            Benchmark Data: {benchmark_data}
            """
            
            prompt = """
            Please perform a performance attribution analysis comparing the portfolio to the benchmark.
            
            Analyze:
            1. Asset allocation effect
            2. Security selection effect
            3. Interaction effect
            4. Total active return decomposition
            5. Sources of outperformance/underperformance
            
            Provide detailed breakdown and insights.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="portfolio",
                context=context
            )
            
            return f"Performance Attribution (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in performance attribution: {e}")
            return f"Error in performance attribution: {str(e)}"
