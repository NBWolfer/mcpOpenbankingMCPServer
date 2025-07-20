#!/usr/bin/env python3
"""
OpenBanking MCP Server
Main entry point for the MCP server with Ollama LLM integration
"""

import asyncio
import logging
from typing import Optional
import argparse
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mcp.server import Server
from mcp.server.stdio import stdio_server

from agents.agent_manager import AgentManager
from tools.tool_registry import ToolRegistry
from config.config import Config


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPOpenbankingServer:
    """Main MCP Server class"""
    
    def __init__(self, config: Config):
        self.config = config
        self.server = Server("openbanking-mcp")
        self.agent_manager = AgentManager(config)
        self.tool_registry = ToolRegistry(self.agent_manager)
        self.app = FastAPI(title="OpenBanking MCP Server")
        
        # Add CORS middleware to allow connections from your backend
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
    async def initialize(self):
        """Initialize the server and all components"""
        try:
            # Initialize agent manager
            await self.agent_manager.initialize()
            
            # Register all tools
            await self.tool_registry.register_tools(self.server)
            
            logger.info("MCP OpenBanking Server initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize server: {e}")
            raise
    
    async def setup_http_endpoints(self):
        """Setup HTTP endpoints for MCP communication"""
        
        @self.app.post("/mcp/call")
        async def call_tool(request_data: dict):
            """Call MCP tools via HTTP"""
            try:
                tool_name = request_data.get("tool_name")
                arguments = request_data.get("arguments", {})
                customer_oid = request_data.get("customer_oid") or request_data.get("CustomerOID")
                
                # Add CustomerOID to arguments if provided
                if customer_oid:
                    arguments["customer_oid"] = customer_oid
                    arguments["CustomerOID"] = customer_oid
                
                # Get the appropriate agent for the tool
                agent = self.agent_manager.get_agent_for_tool(tool_name)
                if not agent:
                    return {"error": f"No agent available for tool: {tool_name}"}
                
                # Execute the tool
                result = await agent.execute_tool(tool_name, arguments)
                return {"result": result}
                
            except Exception as e:
                logger.error(f"Error calling tool: {e}")
                return {"error": str(e)}
        
        @self.app.post("/mcp/query")
        async def query_agent(request_data: dict):
            """Query a specific agent"""
            try:
                agent_type = request_data.get("agent_type", "market_analyst")
                query = request_data.get("query")
                customer_oid = request_data.get("customer_oid") or request_data.get("CustomerOID")
                context = request_data.get("context")
                
                if not query:
                    return {"error": "Query is required"}
                
                agent = self.agent_manager.get_agent(agent_type)
                if not agent:
                    return {"error": f"Agent not found: {agent_type}"}
                
                response = await agent.generate_response(
                    query, 
                    context=context, 
                    customer_oid=customer_oid
                )
                return {"response": response}
                
            except Exception as e:
                logger.error(f"Error querying agent: {e}")
                return {"error": str(e)}
        
        @self.app.get("/mcp/status")
        async def get_status():
            """Get server status"""
            try:
                agents_status = {}
                for agent_name, agent in self.agent_manager.agents.items():
                    agents_status[agent_name] = {
                        "available": agent.is_available,
                        "model": agent.model_name
                    }
                
                return {
                    "status": "running",
                    "agents": agents_status,
                    "tools": list(self.tool_registry.registered_tools.keys())
                }
            except Exception as e:
                logger.error(f"Error getting status: {e}")
                return {"error": str(e)}
        
        @self.app.get("/mcp/customer/{customer_oid}")
        async def get_customer_data(customer_oid: str):
            """Get customer data from bank API"""
            try:
                bank_client = self.agent_manager.bank_api_client
                customer_data = await bank_client.get_comprehensive_customer_data(customer_oid)
                return customer_data
            except Exception as e:
                logger.error(f"Error getting customer data: {e}")
                return {"error": str(e)}
        
        @self.app.post("/mcp/analyze")
        async def analyze_customer(request_data: dict):
            """Perform comprehensive customer analysis using best agent"""
            try:
                customer_oid = request_data.get("customer_oid") or request_data.get("CustomerOID")
                analysis_type = request_data.get("analysis_type", "comprehensive")
                
                if not customer_oid:
                    return {"error": "CustomerOID is required"}
                
                # Choose agent based on analysis type
                agent_mapping = {
                    "portfolio": "portfolio_manager",
                    "risk": "risk_analyst", 
                    "market": "market_analyst",
                    "comprehensive": "explainability_agent"
                }
                
                agent_name = agent_mapping.get(analysis_type, "explainability_agent")
                agent = self.agent_manager.get_agent(agent_name)
                
                if not agent:
                    return {"error": f"Agent not available: {agent_name}"}
                
                prompt = f"Provide a {analysis_type} analysis for this customer's financial situation."
                response = await agent.generate_response(prompt, customer_oid=customer_oid)
                
                return {
                    "customer_oid": customer_oid,
                    "analysis_type": analysis_type,
                    "agent_used": agent_name,
                    "analysis": response
                }
                
            except Exception as e:
                logger.error(f"Error performing customer analysis: {e}")
                return {"error": str(e)}
    
    async def run_stdio(self):
        """Run the MCP server with stdio transport"""
        try:
            await self.initialize()
            
            # Run the server with stdio transport
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
                
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise
    
    async def run_http(self, host: str = "127.0.0.1", port: int = 8001):
        """Run the MCP server with HTTP transport"""
        try:
            await self.initialize()
            await self.setup_http_endpoints()
            
            logger.info(f"Starting MCP server on http://{host}:{port}")
            logger.info("Endpoints available:")
            logger.info(f"  POST http://{host}:{port}/mcp/call - Call MCP tools")
            logger.info(f"  POST http://{host}:{port}/mcp/query - Query agents")
            logger.info(f"  GET  http://{host}:{port}/mcp/status - Server status")
            
            config = uvicorn.Config(
                app=self.app,
                host=host,
                port=port,
                log_level="info"
            )
            server = uvicorn.Server(config)
            await server.serve()
            
        except Exception as e:
            logger.error(f"HTTP Server error: {e}")
            raise


async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="OpenBanking MCP Server")
    parser.add_argument(
        "--dev", 
        action="store_true", 
        help="Run in development mode"
    )
    parser.add_argument(
        "--config", 
        type=str, 
        default="../config/config.yaml",
        help="Configuration file path"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["stdio", "http"],
        default="http",
        help="Server transport mode (stdio for MCP clients, http for web backends)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind HTTP server (only for http mode)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="Port to bind HTTP server (only for http mode)"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = Config.load(args.config)
    if args.dev:
        config.development_mode = True
        
    # Create server
    server = MCPOpenbankingServer(config)
    
    # Run in appropriate mode
    if args.mode == "stdio":
        logger.info("Starting MCP server in stdio mode (for MCP clients)")
        await server.run_stdio()
    else:
        logger.info(f"Starting MCP server in HTTP mode on {args.host}:{args.port}")
        await server.run_http(args.host, args.port)


if __name__ == "__main__":
    asyncio.run(main())
