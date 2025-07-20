"""
Example structure for your dummy bank API
This shows the expected format for your bank API responses that the MCP server will consume
"""

# Example Bank API Endpoints and Response Formats

"""
1. GET /api/customers/{CustomerOID}
Expected Response:
"""
customer_example = {
    "customer_oid": "CUST123456",
    "profile": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "date_of_birth": "1985-05-15",
        "risk_tolerance": "moderate",
        "investment_experience": "intermediate",
        "annual_income": 75000,
        "net_worth": 150000,
        "investment_goals": ["retirement", "wealth_building"],
        "time_horizon": "long_term"
    },
    "preferences": {
        "communication_method": "email",
        "portfolio_style": "balanced",
        "esg_investing": True
    }
}

"""
2. GET /api/portfolio/{CustomerOID}
Expected Response:
"""
portfolio_example = {
    "customer_oid": "CUST123456",
    "total_value": 85000.50,
    "cash_balance": 5000.00,
    "holdings": [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "quantity": 50,
            "current_price": 175.50,
            "market_value": 8775.00,
            "percentage": 10.3,
            "avg_cost": 150.00,
            "unrealized_gain_loss": 1275.00
        },
        {
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "quantity": 20,
            "current_price": 140.75,
            "market_value": 2815.00,
            "percentage": 3.3,
            "avg_cost": 135.00,
            "unrealized_gain_loss": 115.00
        },
        {
            "symbol": "VTSAX",
            "name": "Vanguard Total Stock Market Index",
            "quantity": 500,
            "current_price": 120.45,
            "market_value": 60225.00,
            "percentage": 70.9,
            "avg_cost": 115.00,
            "unrealized_gain_loss": 2725.00
        }
    ],
    "allocation": {
        "stocks": 85.2,
        "bonds": 10.5,
        "cash": 4.3,
        "other": 0.0
    },
    "performance": {
        "today_change": 125.50,
        "today_change_percent": 0.15,
        "mtd_change": 1250.00,
        "mtd_change_percent": 1.5,
        "ytd_change": 8500.00,
        "ytd_change_percent": 11.1
    }
}

"""
3. GET /api/accounts/{CustomerOID}
Expected Response:
"""
accounts_example = {
    "customer_oid": "CUST123456",
    "accounts": [
        {
            "account_id": "ACC789123",
            "account_type": "investment",
            "account_name": "Investment Account",
            "balance": 85000.50,
            "currency": "USD",
            "status": "active"
        },
        {
            "account_id": "ACC789124",
            "account_type": "checking",
            "account_name": "Primary Checking",
            "balance": 15000.00,
            "currency": "USD",
            "status": "active"
        },
        {
            "account_id": "ACC789125",
            "account_type": "savings",
            "account_name": "Emergency Fund",
            "balance": 25000.00,
            "currency": "USD",
            "status": "active"
        }
    ],
    "total_assets": 125000.50
}

"""
4. GET /api/transactions/{CustomerOID}?limit=50
Expected Response:
"""
transactions_example = {
    "customer_oid": "CUST123456",
    "transactions": [
        {
            "transaction_id": "TXN001",
            "date": "2025-07-19",
            "type": "buy",
            "symbol": "AAPL",
            "quantity": 10,
            "price": 175.50,
            "amount": 1755.00,
            "fees": 0.99,
            "account_id": "ACC789123"
        },
        {
            "transaction_id": "TXN002",
            "date": "2025-07-18",
            "type": "dividend",
            "symbol": "VTSAX",
            "quantity": 0,
            "price": 0,
            "amount": 125.50,
            "fees": 0,
            "account_id": "ACC789123"
        },
        {
            "transaction_id": "TXN003",
            "date": "2025-07-17",
            "type": "deposit",
            "symbol": None,
            "quantity": 0,
            "price": 0,
            "amount": 2000.00,
            "fees": 0,
            "account_id": "ACC789123"
        }
    ],
    "pagination": {
        "current_page": 1,
        "per_page": 50,
        "total_transactions": 245
    }
}

"""
5. GET /api/risk/{CustomerOID}
Expected Response:
"""
risk_metrics_example = {
    "customer_oid": "CUST123456",
    "risk_profile": {
        "risk_score": 6.5,
        "risk_category": "moderate",
        "volatility": 0.15,
        "beta": 1.05,
        "sharpe_ratio": 1.2,
        "max_drawdown": -0.08
    },
    "var_analysis": {
        "1_day_var_95": -850.00,
        "1_day_var_99": -1200.00,
        "10_day_var_95": -2685.00,
        "10_day_var_99": -3795.00
    },
    "stress_tests": {
        "market_crash_2008": -12750.00,
        "covid_crash_2020": -8500.00,
        "tech_bubble_2000": -15300.00
    },
    "diversification": {
        "sector_concentration": 0.35,
        "geographic_concentration": 0.8,
        "correlation_risk": 0.6
    }
}

"""
6. GET /api/market-data?symbols=AAPL,GOOGL,VTSAX
Expected Response:
"""
market_data_example = {
    "timestamp": "2025-07-20T11:08:49Z",
    "market_data": [
        {
            "symbol": "AAPL",
            "price": 175.50,
            "change": 2.15,
            "change_percent": 1.24,
            "volume": 45678900,
            "market_cap": 2750000000000,
            "pe_ratio": 28.5,
            "dividend_yield": 0.48
        },
        {
            "symbol": "GOOGL",
            "price": 140.75,
            "change": -1.25,
            "change_percent": -0.88,
            "volume": 23456789,
            "market_cap": 1850000000000,
            "pe_ratio": 25.2,
            "dividend_yield": 0.0
        },
        {
            "symbol": "VTSAX",
            "price": 120.45,
            "change": 0.85,
            "change_percent": 0.71,
            "volume": 1234567,
            "market_cap": None,
            "pe_ratio": None,
            "dividend_yield": 1.8
        }
    ],
    "market_indices": {
        "SPY": {
            "price": 445.50,
            "change": 3.25,
            "change_percent": 0.73
        },
        "QQQ": {
            "price": 375.25,
            "change": -2.15,
            "change_percent": -0.57
        }
    }
}
