"""
Utilities for the MCP OpenBanking Server
"""

import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime


logger = logging.getLogger(__name__)


class DataFormatter:
    """Utility class for formatting data"""
    
    @staticmethod
    def format_portfolio_data(data: Dict[str, Any]) -> str:
        """Format portfolio data for display"""
        try:
            formatted = []
            
            if 'holdings' in data:
                formatted.append("📊 Portfolio Holdings:")
                for holding in data['holdings']:
                    symbol = holding.get('symbol', 'Unknown')
                    weight = holding.get('weight', 0)
                    value = holding.get('value', 0)
                    formatted.append(f"  • {symbol}: {weight:.2%} (${value:,.2f})")
            
            if 'performance' in data:
                perf = data['performance']
                formatted.append("\n📈 Performance Metrics:")
                if 'total_return' in perf:
                    formatted.append(f"  • Total Return: {perf['total_return']:.2%}")
                if 'volatility' in perf:
                    formatted.append(f"  • Volatility: {perf['volatility']:.2%}")
                if 'sharpe_ratio' in perf:
                    formatted.append(f"  • Sharpe Ratio: {perf['sharpe_ratio']:.3f}")
            
            return "\n".join(formatted)
            
        except Exception as e:
            logger.error(f"Error formatting portfolio data: {e}")
            return f"Error formatting data: {str(e)}"
    
    @staticmethod
    def format_market_data(data: Dict[str, Any]) -> str:
        """Format market data for display"""
        try:
            formatted = []
            
            if 'symbols' in data:
                formatted.append("📊 Market Data:")
                for symbol_data in data['symbols']:
                    symbol = symbol_data.get('symbol', 'Unknown')
                    price = symbol_data.get('price', 0)
                    change = symbol_data.get('change', 0)
                    change_pct = symbol_data.get('change_pct', 0)
                    
                    emoji = "🟢" if change >= 0 else "🔴"
                    formatted.append(f"  {emoji} {symbol}: ${price:.2f} ({change:+.2f}, {change_pct:+.2%})")
            
            return "\n".join(formatted)
            
        except Exception as e:
            logger.error(f"Error formatting market data: {e}")
            return f"Error formatting data: {str(e)}"


class ResponseValidator:
    """Utility class for validating responses"""
    
    @staticmethod
    def validate_portfolio_data(data: Any) -> bool:
        """Validate portfolio data structure"""
        if not isinstance(data, dict):
            return False
        
        # Check for required fields
        required_fields = ['holdings']
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate holdings structure
        holdings = data['holdings']
        if not isinstance(holdings, list):
            return False
        
        for holding in holdings:
            if not isinstance(holding, dict):
                return False
            if 'symbol' not in holding:
                return False
        
        return True
    
    @staticmethod
    def validate_user_profile(data: Any) -> bool:
        """Validate user profile data structure"""
        if not isinstance(data, dict):
            return False
        
        # Optional but expected fields
        expected_fields = ['risk_tolerance', 'investment_horizon', 'goals']
        
        return True  # For now, accept any dict structure


class ErrorHandler:
    """Utility class for handling errors"""
    
    @staticmethod
    def handle_agent_error(agent_name: str, error: Exception) -> str:
        """Handle agent-related errors"""
        error_msg = f"Agent '{agent_name}' encountered an error: {str(error)}"
        logger.error(error_msg)
        
        # Provide user-friendly error message
        return f"I'm sorry, but I encountered an issue while processing your request. The {agent_name} agent is currently unavailable. Please try again later or contact support if the issue persists."
    
    @staticmethod
    def handle_tool_error(tool_name: str, error: Exception) -> str:
        """Handle tool-related errors"""
        error_msg = f"Tool '{tool_name}' encountered an error: {str(error)}"
        logger.error(error_msg)
        
        return f"I encountered an issue while using the {tool_name} tool. Please check your input data and try again."


class ConfigValidator:
    """Utility class for validating configuration"""
    
    @staticmethod
    def validate_agent_config(config: Dict[str, Any]) -> List[str]:
        """Validate agent configuration and return list of issues"""
        issues = []
        
        required_fields = ['name', 'model', 'role', 'system_prompt']
        for field in required_fields:
            if field not in config:
                issues.append(f"Missing required field: {field}")
        
        # Validate data types
        if 'temperature' in config:
            temp = config['temperature']
            if not isinstance(temp, (int, float)) or temp < 0 or temp > 2:
                issues.append("Temperature must be a number between 0 and 2")
        
        if 'max_tokens' in config:
            max_tokens = config['max_tokens']
            if not isinstance(max_tokens, int) or max_tokens <= 0:
                issues.append("max_tokens must be a positive integer")
        
        return issues
    
    @staticmethod
    def validate_ollama_config(config: Dict[str, Any]) -> List[str]:
        """Validate Ollama configuration"""
        issues = []
        
        if 'host' not in config:
            issues.append("Missing Ollama host configuration")
        
        if 'port' in config:
            port = config['port']
            if not isinstance(port, int) or port <= 0 or port > 65535:
                issues.append("Port must be a valid integer between 1 and 65535")
        
        return issues


class Logger:
    """Utility class for logging setup"""
    
    @staticmethod
    def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
        """Setup logging configuration"""
        
        # Convert string level to logging constant
        numeric_level = getattr(logging, level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {level}')
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        
        # Setup root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(numeric_level)
        root_logger.addHandler(console_handler)
        
        # Setup file handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
