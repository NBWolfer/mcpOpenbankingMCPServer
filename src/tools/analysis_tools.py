"""
Analysis and explainability tools
"""

import logging
from typing import Dict, Any
from agents.agent_manager import AgentManager


logger = logging.getLogger(__name__)


class AnalysisTools:
    """Tools for analysis and explainability"""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
    
    async def swot_analysis(self, subject: str, context: Dict[str, Any]) -> str:
        """Perform SWOT analysis"""
        try:
            context_str = f"Subject: {subject}\nContext: {context}"
            
            prompt = f"""
            Please perform a comprehensive SWOT analysis for: {subject}
            
            Analyze and provide detailed insights for:
            
            STRENGTHS:
            - Internal positive factors
            - Competitive advantages
            - Unique capabilities
            - Strong performance areas
            
            WEAKNESSES:
            - Internal limitations
            - Areas for improvement
            - Competitive disadvantages
            - Resource constraints
            
            OPPORTUNITIES:
            - External positive factors
            - Market trends
            - Growth potential
            - Emerging possibilities
            
            THREATS:
            - External challenges
            - Market risks
            - Competitive pressures
            - Economic/regulatory risks
            
            Provide specific, actionable insights for each category and strategic recommendations.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="swot",
                context=context_str
            )
            
            return f"SWOT Analysis (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in SWOT analysis: {e}")
            return f"Error performing SWOT analysis: {str(e)}"
    
    async def explain_concept(self, concept: str, complexity_level: str = "intermediate") -> str:
        """Explain financial concepts in simple terms"""
        try:
            context = f"Concept: {concept}\nComplexity Level: {complexity_level}"
            
            prompt = f"""
            Please explain the financial concept "{concept}" at a {complexity_level} level.
            
            Structure your explanation to include:
            1. Simple definition in everyday language
            2. Key components or characteristics
            3. Why it matters in finance/investing
            4. Real-world examples
            5. Common misconceptions
            6. Practical applications
            7. Related concepts to explore further
            
            Make the explanation clear, engaging, and educational while maintaining accuracy.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="explanation",
                context=context
            )
            
            return f"Concept Explanation (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error explaining concept: {e}")
            return f"Error explaining concept: {str(e)}"
    
    async def reverse_simulation(self, target_outcome: Dict[str, Any], current_state: Dict[str, Any]) -> str:
        """Perform reverse simulation analysis"""
        try:
            context = f"""
            Target Outcome: {target_outcome}
            Current State: {current_state}
            """
            
            prompt = f"""
            Please perform a reverse simulation analysis to determine how to achieve the target outcome from the current state.
            
            Analyze:
            1. Gap analysis between current state and target
            2. Required steps and milestones
            3. Timeline and sequencing
            4. Resource requirements
            5. Potential obstacles and solutions
            6. Alternative pathways
            7. Risk factors and mitigation strategies
            8. Success probability assessment
            9. Key performance indicators to monitor
            10. Contingency plans
            
            Provide a detailed roadmap with specific, actionable recommendations.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="explanation",
                context=context
            )
            
            return f"Reverse Simulation (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in reverse simulation: {e}")
            return f"Error performing reverse simulation: {str(e)}"
    
    async def decision_analysis(self, decision_context: Dict[str, Any], options: list) -> str:
        """Analyze decision options and provide recommendations"""
        try:
            context = f"""
            Decision Context: {decision_context}
            Available Options: {options}
            """
            
            prompt = f"""
            Please analyze the decision options and provide a comprehensive recommendation.
            
            For each option, evaluate:
            1. Pros and cons
            2. Risk-return profile
            3. Alignment with objectives
            4. Implementation complexity
            5. Resource requirements
            6. Timeline implications
            7. Potential outcomes and scenarios
            
            Then provide:
            - Comparative analysis
            - Recommended option with rationale
            - Implementation considerations
            - Monitoring and review framework
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="explanation",
                context=context
            )
            
            return f"Decision Analysis (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in decision analysis: {e}")
            return f"Error analyzing decision: {str(e)}"
    
    async def trend_analysis(self, data_context: Dict[str, Any], trend_type: str = "general") -> str:
        """Analyze trends and patterns in data"""
        try:
            context = f"""
            Data Context: {data_context}
            Trend Analysis Type: {trend_type}
            """
            
            prompt = f"""
            Please analyze the trends and patterns in the provided data.
            
            Focus on:
            1. Trend identification (upward, downward, sideways)
            2. Trend strength and momentum
            3. Cyclical patterns
            4. Seasonal effects
            5. Breakout/breakdown points
            6. Support and resistance levels
            7. Leading and lagging indicators
            8. Future trend projections
            9. Risk factors for trend reversal
            
            Provide actionable insights based on the trend analysis.
            """
            
            agent_name, response = await self.agent_manager.query_best_agent(
                prompt=prompt,
                task_type="explanation",
                context=context
            )
            
            return f"Trend Analysis (by {agent_name}):\n\n{response}"
            
        except Exception as e:
            logger.error(f"Error in trend analysis: {e}")
            return f"Error analyzing trends: {str(e)}"
