"""
Risk assessment and management tools
"""

import logging
from typing import Dict, Any, List
from agents.agent_manager import AgentManager


logger = logging.getLogger(__name__)


class RiskTools:
    """Tools for risk assessment and management"""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
    
    async def assess_risk(
        self, 
        portfolio_data: Dict[str, Any], 
        user_profile: Dict[str, Any], 
        risk_type: str = "comprehensive"
    ) -> str:
        """Assess risk for user portfolio"""
        try:
            context = f"""
            Portfolio Data: {portfolio_data}
            User Profile: {user_profile}
            Risk Assessment Type: {risk_type}
            """
            
            prompt = f"""
            Please perform a comprehensive risk assessment for the user's portfolio.
            
            Analyze:
            1. Portfolio risk metrics (VaR, CVaR, volatility, beta)
            2. Concentration risk and diversification analysis
            3. Liquidity risk assessment
            4. Market risk exposure
            5. Credit risk (if applicable)
            6. User-specific risk tolerance alignment
            7. Risk-adjusted performance measures
            8. Stress testing under various scenarios
            
            Provide personalized risk recommendations based on the user's profile.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="risk",
                context=context
            )
            
            return f"Risk Assessment (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in risk assessment: {e}")
            return f"Error assessing risk: {str(e)}"
    
    async def simulate_scenarios(self, portfolio_data: Dict[str, Any], scenarios: List[Dict[str, Any]]) -> str:
        """Run risk simulation scenarios"""
        try:
            context = f"""
            Portfolio Data: {portfolio_data}
            Simulation Scenarios: {scenarios}
            """
            
            prompt = f"""
            Please run scenario analysis and stress testing for the portfolio.
            
            For each scenario, analyze:
            1. Expected portfolio impact
            2. Worst-case and best-case outcomes
            3. Probability of occurrence
            4. Portfolio resilience
            5. Required hedging strategies
            6. Recovery time estimates
            7. Liquidity implications
            
            Provide actionable recommendations for risk mitigation.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="risk",
                context=context
            )
            
            return f"Scenario Analysis (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in scenario simulation: {e}")
            return f"Error running scenario simulation: {str(e)}"
    
    async def liquidity_risk_analysis(self, portfolio_data: Dict[str, Any]) -> str:
        """Analyze liquidity risk of the portfolio"""
        try:
            context = f"Portfolio Data: {portfolio_data}"
            
            prompt = f"""
            Please analyze the liquidity risk characteristics of the portfolio.
            
            Examine:
            1. Asset liquidity profiles
            2. Market depth and trading volumes
            3. Bid-ask spreads and market impact
            4. Liquidity during stress periods
            5. Redemption and margin call risks
            6. Liquidity diversification
            7. Emergency liquidation strategies
            
            Provide recommendations for liquidity management.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="risk",
                context=context
            )
            
            return f"Liquidity Risk Analysis (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in liquidity risk analysis: {e}")
            return f"Error analyzing liquidity risk: {str(e)}"
    
    async def tail_risk_analysis(self, portfolio_data: Dict[str, Any]) -> str:
        """Analyze tail risk and extreme events"""
        try:
            context = f"Portfolio Data: {portfolio_data}"
            
            prompt = f"""
            Please analyze the tail risk characteristics of the portfolio.
            
            Focus on:
            1. Value at Risk (VaR) at different confidence levels
            2. Conditional Value at Risk (CVaR/Expected Shortfall)
            3. Maximum drawdown analysis
            4. Fat tail and skewness characteristics
            5. Extreme event probability estimation
            6. Tail hedging strategies
            7. Black swan event preparedness
            
            Identify portfolio vulnerabilities to extreme market events.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="risk",
                context=context
            )
            
            return f"Tail Risk Analysis (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in tail risk analysis: {e}")
            return f"Error analyzing tail risk: {str(e)}"
