"""
Example usage of MCP Server from your backend on port 8000
This demonstrates how to interact with the MCP server using CustomerOID
"""

import asyncio
import httpx
import json


class MCPClientExample:
    """Example client for interacting with MCP server"""
    
    def __init__(self, mcp_server_url: str = "http://127.0.0.1:8001"):
        self.mcp_server_url = mcp_server_url
        
    async def check_server_status(self):
        """Check if MCP server is running"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.mcp_server_url}/mcp/status")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": f"Server not available: {e}"}
    
    async def get_customer_data(self, customer_oid: str):
        """Get customer data from bank API via MCP server"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.mcp_server_url}/mcp/customer/{customer_oid}")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": f"Failed to get customer data: {e}"}
    
    async def query_agent(self, agent_type: str, query: str, customer_oid: str):
        """Query a specific agent with customer context"""
        try:
            payload = {
                "agent_type": agent_type,
                "query": query,
                "customer_oid": customer_oid
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.mcp_server_url}/mcp/query",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": f"Failed to query agent: {e}"}
    
    async def call_tool(self, tool_name: str, arguments: dict, customer_oid: str):
        """Call an MCP tool with customer context"""
        try:
            payload = {
                "tool_name": tool_name,
                "arguments": arguments,
                "customer_oid": customer_oid
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.mcp_server_url}/mcp/call",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": f"Failed to call tool: {e}"}
    
    async def analyze_customer(self, customer_oid: str, analysis_type: str = "comprehensive"):
        """Perform comprehensive customer analysis"""
        try:
            payload = {
                "customer_oid": customer_oid,
                "analysis_type": analysis_type
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.mcp_server_url}/mcp/analyze",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": f"Failed to analyze customer: {e}"}


async def demo_usage():
    """Demonstrate MCP server usage"""
    client = MCPClientExample()
    customer_oid = "CUST123456"  # Example CustomerOID
    
    print("=== MCP Server Demo ===")
    
    # 1. Check server status
    print("\n1. Checking server status...")
    status = await client.check_server_status()
    print(json.dumps(status, indent=2))
    
    # 2. Get customer data (this will fail until you have the dummy bank API running)
    print(f"\n2. Getting customer data for {customer_oid}...")
    customer_data = await client.get_customer_data(customer_oid)
    print(json.dumps(customer_data, indent=2))
    
    # 3. Query portfolio manager about the customer
    print(f"\n3. Querying portfolio manager for {customer_oid}...")
    portfolio_query = await client.query_agent(
        agent_type="portfolio_manager",
        query="Analyze my portfolio and suggest improvements",
        customer_oid=customer_oid
    )
    print(json.dumps(portfolio_query, indent=2))
    
    # 4. Call a portfolio analysis tool
    print(f"\n4. Calling portfolio analysis tool for {customer_oid}...")
    tool_result = await client.call_tool(
        tool_name="analyze_portfolio",
        arguments={"analysis_type": "comprehensive"},
        customer_oid=customer_oid
    )
    print(json.dumps(tool_result, indent=2))
    
    # 5. Perform comprehensive analysis
    print(f"\n5. Performing comprehensive analysis for {customer_oid}...")
    analysis = await client.analyze_customer(customer_oid, "comprehensive")
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    asyncio.run(demo_usage())
