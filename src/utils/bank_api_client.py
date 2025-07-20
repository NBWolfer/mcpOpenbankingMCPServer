"""
Bank API Client for fetching customer data from dummy bank API
"""

import asyncio
import logging
import httpx
from typing import Dict, Any, Optional, List
from config.config import BankApiConfig


logger = logging.getLogger(__name__)


class BankApiClient:
    """Client for communicating with the dummy bank API"""
    
    def __init__(self, config: BankApiConfig):
        self.config = config
        self.base_url = config.base_url
        self.timeout = config.timeout
        self.api_key = config.api_key
        self.endpoints = config.endpoints
    
    async def _make_request(
        self, 
        endpoint: str, 
        method: str = "GET", 
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to bank API"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Add API key if configured
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            url = f"{self.base_url}{endpoint}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if method.upper() == "GET":
                    response = await client.get(url, headers=headers)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=headers, json=data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}: {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error for {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {e}")
            raise
    
    async def get_customer_data(self, customer_oid: str) -> Dict[str, Any]:
        """Get customer profile data"""
        try:
            endpoint = self.endpoints["customer"].format(CustomerOID=customer_oid)
            data = await self._make_request(endpoint)
            logger.info(f"Retrieved customer data for {customer_oid}")
            return data
        except Exception as e:
            logger.error(f"Failed to get customer data for {customer_oid}: {e}")
            return {"error": f"Failed to retrieve customer data: {str(e)}"}
    
    async def get_portfolio_data(self, customer_oid: str) -> Dict[str, Any]:
        """Get customer portfolio data"""
        try:
            endpoint = self.endpoints["portfolio"].format(CustomerOID=customer_oid)
            data = await self._make_request(endpoint)
            logger.info(f"Retrieved portfolio data for {customer_oid}")
            return data
        except Exception as e:
            logger.error(f"Failed to get portfolio data for {customer_oid}: {e}")
            return {"error": f"Failed to retrieve portfolio data: {str(e)}"}
    
    async def get_transactions(self, customer_oid: str, limit: int = 100) -> Dict[str, Any]:
        """Get customer transaction history"""
        try:
            endpoint = self.endpoints["transactions"].format(CustomerOID=customer_oid)
            if limit:
                endpoint += f"?limit={limit}"
            
            data = await self._make_request(endpoint)
            logger.info(f"Retrieved {len(data.get('transactions', []))} transactions for {customer_oid}")
            return data
        except Exception as e:
            logger.error(f"Failed to get transactions for {customer_oid}: {e}")
            return {"error": f"Failed to retrieve transactions: {str(e)}"}
    
    async def get_accounts(self, customer_oid: str) -> Dict[str, Any]:
        """Get customer account information"""
        try:
            endpoint = self.endpoints["accounts"].format(CustomerOID=customer_oid)
            data = await self._make_request(endpoint)
            logger.info(f"Retrieved account data for {customer_oid}")
            return data
        except Exception as e:
            logger.error(f"Failed to get accounts for {customer_oid}: {e}")
            return {"error": f"Failed to retrieve accounts: {str(e)}"}
    
    async def get_market_data(self, symbols: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get general market data (not customer-specific)"""
        try:
            endpoint = self.endpoints["market_data"]
            if symbols:
                endpoint += f"?symbols={','.join(symbols)}"
            
            data = await self._make_request(endpoint)
            logger.info("Retrieved market data")
            return data
        except Exception as e:
            logger.error(f"Failed to get market data: {e}")
            return {"error": f"Failed to retrieve market data: {str(e)}"}
    
    async def get_risk_metrics(self, customer_oid: str) -> Dict[str, Any]:
        """Get customer risk metrics"""
        try:
            endpoint = self.endpoints["risk_metrics"].format(CustomerOID=customer_oid)
            data = await self._make_request(endpoint)
            logger.info(f"Retrieved risk metrics for {customer_oid}")
            return data
        except Exception as e:
            logger.error(f"Failed to get risk metrics for {customer_oid}: {e}")
            return {"error": f"Failed to retrieve risk metrics: {str(e)}"}
    
    async def get_comprehensive_customer_data(self, customer_oid: str) -> Dict[str, Any]:
        """Get all customer data in one call"""
        try:
            # Make parallel requests for all customer data
            customer_task = self.get_customer_data(customer_oid)
            portfolio_task = self.get_portfolio_data(customer_oid)
            accounts_task = self.get_accounts(customer_oid)
            transactions_task = self.get_transactions(customer_oid, limit=50)
            risk_task = self.get_risk_metrics(customer_oid)
            
            # Wait for all requests to complete
            customer_data, portfolio_data, accounts_data, transactions_data, risk_data = await asyncio.gather(
                customer_task,
                portfolio_task,
                accounts_task,
                transactions_task,
                risk_task,
                return_exceptions=True
            )
            
            # Compile comprehensive data
            comprehensive_data = {
                "customer_oid": customer_oid,
                "customer": customer_data if not isinstance(customer_data, Exception) else {"error": str(customer_data)},
                "portfolio": portfolio_data if not isinstance(portfolio_data, Exception) else {"error": str(portfolio_data)},
                "accounts": accounts_data if not isinstance(accounts_data, Exception) else {"error": str(accounts_data)},
                "transactions": transactions_data if not isinstance(transactions_data, Exception) else {"error": str(transactions_data)},
                "risk_metrics": risk_data if not isinstance(risk_data, Exception) else {"error": str(risk_data)}
            }
            
            logger.info(f"Retrieved comprehensive data for {customer_oid}")
            return comprehensive_data
            
        except Exception as e:
            logger.error(f"Failed to get comprehensive data for {customer_oid}: {e}")
            return {"error": f"Failed to retrieve comprehensive customer data: {str(e)}"}
