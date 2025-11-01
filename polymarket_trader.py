"""
Polymarket Trading Bot - Core Trading Module
Provides functionality for buying, selling, and checking portfolio/cash values.
"""

import os
import requests
from typing import Dict, Optional, Any
from decimal import Decimal


class PolymarketTrader:
    """
    Main trading class for Polymarket operations.
    Handles authentication and core trading functions.
    """
    
    BASE_URL = "https://clob.polymarket.com"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Polymarket trader.
        
        Args:
            api_key: Polymarket API key. If not provided, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("POLYMARKET_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Provide it as parameter or set POLYMARKET_API_KEY environment variable."
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an authenticated request to the Polymarket API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            **kwargs: Additional arguments for requests
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.exceptions.RequestException: If request fails
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def get_portfolio_value(self) -> Dict[str, Any]:
        """
        Get the total portfolio value including all positions.
        
        Returns:
            Dictionary containing portfolio information including:
            - total_value: Total portfolio value in USD
            - positions: List of positions with details
            - raw_data: Raw API response
        """
        try:
            # Get account balances and positions
            # Note: Actual endpoint may vary - common patterns include /balances, /positions, /portfolio
            response = self._make_request("GET", "balances")
            
            # Calculate portfolio value
            portfolio_data = {
                "total_value": Decimal("0"),
                "positions": [],
                "raw_data": response
            }
            
            # Process positions if available
            # Handle different possible response structures
            balances = []
            if isinstance(response, dict):
                balances = response.get("balances", response.get("positions", response.get("data", [])))
            elif isinstance(response, list):
                balances = response
            
            for balance in balances:
                if balance.get("token") != "USDC":  # Exclude cash
                    portfolio_data["positions"].append(balance)
            
            # Calculate total value (simplified - would need market prices for accurate calculation)
            portfolio_data["total_value"] = sum(
                Decimal(str(pos.get("amount", pos.get("balance", 0)))) 
                for pos in portfolio_data["positions"]
            )
            
            return portfolio_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching portfolio: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise
    
    def get_cash_value(self) -> Dict[str, Any]:
        """
        Get the available cash (USDC) balance.
        
        Returns:
            Dictionary containing cash information:
            - cash_balance: Available USDC balance
            - currency: Currency code (USDC)
        """
        try:
            response = self._make_request("GET", "balances")
            
            # Find USDC balance
            cash_data = {
                "cash_balance": Decimal("0"),
                "currency": "USDC"
            }
            
            # Handle different possible response structures
            balances = []
            if isinstance(response, dict):
                balances = response.get("balances", response.get("positions", response.get("data", [])))
            elif isinstance(response, list):
                balances = response
            
            for balance in balances:
                if balance.get("token") == "USDC" or balance.get("currency") == "USDC":
                    cash_data["cash_balance"] = Decimal(str(
                        balance.get("amount", balance.get("balance", balance.get("available", 0)))
                    ))
                    break
            
            return cash_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching cash balance: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise
    
    def buy(self, condition_id: str, outcome: str, amount: Decimal, price: Optional[Decimal] = None) -> Dict[str, Any]:
        """
        Place a buy order on Polymarket.
        
        Args:
            condition_id: The market condition ID
            outcome: The outcome to buy (e.g., "YES" or "NO")
            amount: Amount to buy in shares
            price: Optional price per share. If None, will use market price.
                   Note: Market price fetching needs order book parsing implementation.
            
        Returns:
            Dictionary containing order information:
            - status: Order status
            - order_id: Order ID if successful
            - order_data: Submitted order data
            - raw_response: Raw API response
        """
        try:
            # First, get the current market price if not provided
            if price is None:
                try:
                    market_data = self._make_request("GET", f"markets/{condition_id}")
                    # TODO: Parse order book to get best bid/ask price
                    # For now, this is a placeholder - actual implementation needed
                    price = Decimal("0.5")  # Placeholder
                except:
                    raise ValueError("Price is required. Market price fetching not yet implemented.")
            
            # Construct the order
            # Note: Actual API may require different field names or structure
            order_data = {
                "condition_id": condition_id,
                "outcome": outcome.upper(),
                "side": "BUY",
                "amount": str(amount),
                "price": str(price),
                "type": "LIMIT"  # Can be LIMIT or MARKET
            }
            
            # Place the order
            # Note: Actual endpoint may vary - could be /orders, /trade, /place-order, etc.
            response = self._make_request("POST", "orders", json=order_data)
            
            return {
                "status": "success",
                "order_id": response.get("id", response.get("order_id", response.get("orderId"))),
                "order_data": order_data,
                "raw_response": response
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error placing buy order: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise
    
    def sell(self, condition_id: str, outcome: str, amount: Decimal, price: Optional[Decimal] = None) -> Dict[str, Any]:
        """
        Place a sell order on Polymarket.
        
        Args:
            condition_id: The market condition ID
            outcome: The outcome to sell (e.g., "YES" or "NO")
            amount: Amount to sell in shares
            price: Optional price per share. If None, will use market price.
                   Note: Market price fetching needs order book parsing implementation.
            
        Returns:
            Dictionary containing order information:
            - status: Order status
            - order_id: Order ID if successful
            - order_data: Submitted order data
            - raw_response: Raw API response
        """
        try:
            # First, get the current market price if not provided
            if price is None:
                try:
                    market_data = self._make_request("GET", f"markets/{condition_id}")
                    # TODO: Parse order book to get best bid/ask price
                    # For now, this is a placeholder - actual implementation needed
                    price = Decimal("0.5")  # Placeholder
                except:
                    raise ValueError("Price is required. Market price fetching not yet implemented.")
            
            # Construct the order
            # Note: Actual API may require different field names or structure
            order_data = {
                "condition_id": condition_id,
                "outcome": outcome.upper(),
                "side": "SELL",
                "amount": str(amount),
                "price": str(price),
                "type": "LIMIT"  # Can be LIMIT or MARKET
            }
            
            # Place the order
            # Note: Actual endpoint may vary - could be /orders, /trade, /place-order, etc.
            response = self._make_request("POST", "orders", json=order_data)
            
            return {
                "status": "success",
                "order_id": response.get("id", response.get("order_id", response.get("orderId"))),
                "order_data": order_data,
                "raw_response": response
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error placing sell order: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise
