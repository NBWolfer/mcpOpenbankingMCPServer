#!/usr/bin/env python3
"""
Example usage of the OpenBanking MCP Server
This script demonstrates how to interact with the MCP server programmatically
"""

import asyncio
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.config import Config
from agents.agent_manager import AgentManager
from tools.portfolio_tools import PortfolioTools
from tools.analysis_tools import AnalysisTools


async def demo_portfolio_analysis():
    """Demo portfolio analysis functionality"""
    print("🔄 Demo: Portfolio Analysis")
    print("-" * 30)
    
    # Sample portfolio data
    portfolio_data = {
        "holdings": [
            {"symbol": "AAPL", "weight": 0.30, "value": 30000},
            {"symbol": "GOOGL", "weight": 0.25, "value": 25000},
            {"symbol": "MSFT", "weight": 0.20, "value": 20000},
            {"symbol": "TSLA", "weight": 0.15, "value": 15000},
            {"symbol": "NVDA", "weight": 0.10, "value": 10000}
        ],
        "performance": {
            "total_return": 0.125,
            "volatility": 0.18,
            "sharpe_ratio": 0.85
        }
    }
    
    try:
        config = Config.load("config/config.yaml")
        agent_manager = AgentManager(config)
        
        # Initialize only if Ollama is available
        try:
            await agent_manager.initialize()
            portfolio_tools = PortfolioTools(agent_manager)
            
            result = await portfolio_tools.analyze_portfolio(portfolio_data, "comprehensive")
            print(result)
            
        except Exception as e:
            print(f"⚠ Ollama not available, showing mock analysis: {e}")
            print("""
Portfolio Analysis (Mock):

📊 Portfolio Holdings:
  • AAPL: 30.00% ($30,000.00)
  • GOOGL: 25.00% ($25,000.00)
  • MSFT: 20.00% ($20,000.00)
  • TSLA: 15.00% ($15,000.00)
  • NVDA: 10.00% ($10,000.00)

📈 Performance Metrics:
  • Total Return: 12.50%
  • Volatility: 18.00%
  • Sharpe Ratio: 0.850

Analysis: This portfolio shows strong tech sector concentration with good performance metrics.
Recommendation: Consider diversification across other sectors to reduce risk.
""")
            
    except Exception as e:
        print(f"Error in demo: {e}")


async def demo_swot_analysis():
    """Demo SWOT analysis functionality"""
    print("\n🔄 Demo: SWOT Analysis")
    print("-" * 30)
    
    try:
        config = Config.load("config/config.yaml")
        agent_manager = AgentManager(config)
        
        try:
            await agent_manager.initialize()
            analysis_tools = AnalysisTools(agent_manager)
            
            result = await analysis_tools.swot_analysis(
                "Electric Vehicle Industry",
                {"timeframe": "2024-2025", "market": "global"}
            )
            print(result)
            
        except Exception as e:
            print(f"⚠ Ollama not available, showing mock SWOT: {e}")
            print("""
SWOT Analysis (Mock): Electric Vehicle Industry

STRENGTHS:
• Growing environmental consciousness
• Government incentives and support
• Advancing battery technology
• Lower operating costs

WEAKNESSES:
• High initial purchase price
• Limited charging infrastructure
• Range anxiety among consumers
• Battery replacement costs

OPPORTUNITIES:
• Expanding global market
• Autonomous vehicle integration
• Energy storage applications
• Declining battery costs

THREATS:
• Traditional automaker competition
• Economic downturns affecting adoption
• Raw material supply constraints
• Regulatory changes
""")
            
    except Exception as e:
        print(f"Error in SWOT demo: {e}")


async def demo_risk_assessment():
    """Demo risk assessment functionality"""
    print("\n🔄 Demo: Risk Assessment")
    print("-" * 30)
    
    print("Mock Risk Assessment:")
    print("""
Risk Assessment Report:

🎯 Portfolio Risk Score: 7/10 (Moderate-High Risk)

Key Risk Factors:
• Sector Concentration: High exposure to technology sector (85%)
• Volatility: Above-average portfolio volatility (18%)
• Market Correlation: High correlation with NASDAQ index

Recommendations:
1. Diversify across sectors (healthcare, financials, utilities)
2. Consider adding defensive assets (bonds, REITs)
3. Implement position sizing limits
4. Regular rebalancing schedule

Risk Mitigation Strategies:
• Add low-correlation assets
• Implement stop-loss orders
• Consider hedging strategies
""")


async def main():
    """Run all demos"""
    print("🚀 OpenBanking MCP Server - Demo Examples")
    print("=" * 50)
    
    await demo_portfolio_analysis()
    await demo_swot_analysis() 
    await demo_risk_assessment()
    
    print("\n" + "=" * 50)
    print("✅ Demo completed!")
    print("\nTo start the full MCP server, run:")
    print("  python startup.py")
    print("  or")
    print("  python src/main.py")


if __name__ == "__main__":
    asyncio.run(main())
