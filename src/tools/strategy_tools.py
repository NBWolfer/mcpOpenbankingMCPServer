"""
Strategy recommendation tools
"""

import logging
from typing import Dict, Any, List
from agents.agent_manager import AgentManager


logger = logging.getLogger(__name__)


class StrategyTools:
    """Tools for investment strategy recommendations"""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
    
    async def recommend_strategy(
        self, 
        user_profile: Dict[str, Any], 
        market_conditions: Dict[str, Any], 
        strategy_type: str = "balanced"
    ) -> str:
        """Recommend investment strategy based on user profile and market conditions"""
        try:
            context = f"""
            User Profile: {user_profile}
            Market Conditions: {market_conditions}
            Requested Strategy Type: {strategy_type}
            """
            
            prompt = f"""
            Please recommend a comprehensive investment strategy tailored to the user's profile and current market conditions.
            
            Consider:
            1. User's risk tolerance and investment horizon
            2. Financial goals and constraints
            3. Current market environment
            4. Asset allocation recommendations
            5. Security selection criteria
            6. Timing and implementation considerations
            7. Rebalancing frequency and triggers
            8. Exit strategies and risk management
            
            Provide a detailed, actionable investment strategy with specific recommendations.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="strategy",
                context=context
            )
            
            return f"Strategy Recommendation (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in strategy recommendation: {e}")
            return f"Error recommending strategy: {str(e)}"
    
    async def tactical_allocation(self, market_outlook: Dict[str, Any], current_allocation: Dict[str, Any]) -> str:
        """Provide tactical asset allocation recommendations"""
        try:
            context = f"""
            Market Outlook: {market_outlook}
            Current Allocation: {current_allocation}
            """
            
            prompt = f"""
            Please provide tactical asset allocation recommendations based on the market outlook.
            
            Analyze:
            1. Short-term market opportunities and risks
            2. Sector and regional rotation opportunities
            3. Over/underweight recommendations vs strategic allocation
            4. Duration and magnitude of tactical adjustments
            5. Market timing considerations
            6. Risk management overlays
            7. Implementation costs and logistics
            
            Provide specific allocation targets and rationale for each adjustment.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="strategy",
                context=context
            )
            
            return f"Tactical Allocation (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in tactical allocation: {e}")
            return f"Error providing tactical allocation: {str(e)}"
    
    async def rebalancing_strategy(self, portfolio_data: Dict[str, Any], target_allocation: Dict[str, Any]) -> str:
        """Recommend portfolio rebalancing strategy"""
        try:
            context = f"""
            Current Portfolio: {portfolio_data}
            Target Allocation: {target_allocation}
            """
            
            prompt = f"""
            Please develop a portfolio rebalancing strategy to move from current to target allocation.
            
            Consider:
            1. Deviation from target weights
            2. Transaction costs and market impact
            3. Tax implications (if applicable)
            4. Market timing and execution strategy
            5. Gradual vs immediate rebalancing
            6. Cash flows and new contributions
            7. Threshold-based vs calendar-based rebalancing
            
            Provide a step-by-step rebalancing plan with specific actions.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="strategy",
                context=context
            )
            
            return f"Rebalancing Strategy (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in rebalancing strategy: {e}")
            return f"Error developing rebalancing strategy: {str(e)}"
    
    async def hedge_strategy(self, portfolio_data: Dict[str, Any], hedge_objectives: Dict[str, Any]) -> str:
        """Recommend hedging strategies"""
        try:
            context = f"""
            Portfolio Data: {portfolio_data}
            Hedge Objectives: {hedge_objectives}
            """
            
            prompt = f"""
            Please recommend hedging strategies for the portfolio based on the specified objectives.
            
            Analyze:
            1. Risk exposures requiring hedging
            2. Available hedging instruments
            3. Hedge ratios and effectiveness
            4. Cost-benefit analysis of different approaches
            5. Dynamic vs static hedging strategies
            6. Cross-hedging considerations
            7. Hedge monitoring and adjustment triggers
            
            Provide specific hedging recommendations with implementation details.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="strategy",
                context=context
            )
            
            return f"Hedge Strategy (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in hedge strategy: {e}")
            return f"Error developing hedge strategy: {str(e)}"
