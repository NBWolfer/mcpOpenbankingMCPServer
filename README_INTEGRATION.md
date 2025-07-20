# MCP Server with Bank API Integration

## Overview

This MCP (Model Context Protocol) server integrates with your backend on port 8000 and communicates with your dummy bank API using CustomerOID as the common identifier. The server provides AI-powered financial analysis using 4 specialized agents that can access customer-specific data.

## Architecture

```
Your Backend (Port 8000) --> MCP Server (Port 8001) --> Dummy Bank API (Port 3000)
     |                              |                           |
CustomerOID ----------------------> CustomerOID -------------> CustomerOID
```

## Configuration

### Bank API Settings (config/config.yaml)

```yaml
bank_api:
  base_url: "http://localhost:3000"  # Your dummy bank API
  timeout: 10
  api_key: ""  # Optional authentication
  endpoints:
    customer: "/api/customers/{CustomerOID}"
    portfolio: "/api/portfolio/{CustomerOID}"
    transactions: "/api/transactions/{CustomerOID}"
    accounts: "/api/accounts/{CustomerOID}"
    market_data: "/api/market-data"
    risk_metrics: "/api/risk/{CustomerOID}"
```

## Available Endpoints

### 1. Server Status
- **GET** `/mcp/status`
- Check server health and agent availability

### 2. Query Agent
- **POST** `/mcp/query`
- Body:
```json
{
  "agent_type": "portfolio_manager",
  "query": "Analyze my portfolio and suggest improvements",
  "customer_oid": "CUST123456",
  "context": "Optional additional context"
}
```

### 3. Call Tool
- **POST** `/mcp/call`
- Body:
```json
{
  "tool_name": "analyze_portfolio",
  "arguments": {"analysis_type": "comprehensive"},
  "customer_oid": "CUST123456"
}
```

### 4. Get Customer Data
- **GET** `/mcp/customer/{customer_oid}`
- Retrieves comprehensive customer data from bank API

### 5. Analyze Customer
- **POST** `/mcp/analyze`
- Body:
```json
{
  "customer_oid": "CUST123456",
  "analysis_type": "comprehensive"  // "portfolio", "risk", "market", "comprehensive"
}
```

## Agents

### 1. Market Analyst (`market_analyst`)
- **Role**: Market Data Analyst
- **Specialization**: Market trends, volatility, economic indicators
- **Use Cases**: Market analysis, sentiment analysis, timing strategies

### 2. Portfolio Manager (`portfolio_manager`)
- **Role**: Portfolio Manager
- **Specialization**: Asset allocation, portfolio optimization, strategy development
- **Use Cases**: Portfolio reviews, rebalancing, investment strategies

### 3. Risk Analyst (`risk_analyst`)
- **Role**: Risk Analyst
- **Specialization**: Risk assessment, options strategies, hedging
- **Use Cases**: Risk evaluation, VaR calculations, stress testing

### 4. Explainability Agent (`explainability_agent`)
- **Role**: Explainability & Strategy Agent
- **Specialization**: Making complex concepts understandable
- **Use Cases**: Educational content, strategy explanations, SWOT analysis

## Integration Example

### From Your Backend (Port 8000)

```python
import httpx

async def get_portfolio_analysis(customer_oid: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/mcp/query",
            json={
                "agent_type": "portfolio_manager",
                "query": "Provide a comprehensive portfolio analysis with specific recommendations",
                "customer_oid": customer_oid
            }
        )
        return response.json()

# The MCP server will:
# 1. Receive your request with CustomerOID
# 2. Fetch customer data from your dummy bank API using the CustomerOID
# 3. Use the portfolio_manager agent with customer context
# 4. Return AI-generated analysis based on real customer data
```

## Data Flow

1. **Your Backend** sends request with CustomerOID to MCP server
2. **MCP Server** receives request and extracts CustomerOID
3. **Bank API Client** fetches comprehensive customer data using CustomerOID:
   - Customer profile
   - Portfolio holdings
   - Account information
   - Transaction history
   - Risk metrics
4. **Agent** generates response using:
   - System prompt (role-specific expertise)
   - Customer data context
   - User query
5. **LLM** (Ollama gemma3:4b) processes everything and generates personalized response
6. **Response** sent back to your backend

## Running the Server

### HTTP Mode (for your backend)
```bash
cd src
python main.py --mode http --port 8001
```

### stdio Mode (for MCP clients)
```bash
cd src
python main.py --mode stdio
```

## Required Dependencies

- `ollama` - LLM integration
- `fastapi` - HTTP server
- `uvicorn` - ASGI server
- `httpx` - HTTP client for bank API
- `pyyaml` - Configuration
- `pydantic` - Data validation

## Testing

Use the provided `demo_client.py` to test the integration:

```bash
python demo_client.py
```

This will demonstrate all the available endpoints and show how your backend should interact with the MCP server.

## Error Handling

The server handles various error scenarios:
- Bank API unavailability
- Invalid CustomerOID
- Missing customer data
- LLM generation errors
- Network timeouts

All errors are returned in a consistent format:
```json
{
  "error": "Description of the error"
}
```

## Security Considerations

1. Add authentication between your backend and MCP server
2. Validate CustomerOID format and permissions
3. Implement rate limiting
4. Use HTTPS in production
5. Secure bank API communication
