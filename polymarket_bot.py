"""
Polymarket Trading Bot - Core Functionality
Provides foundational features for automated trading on Polymarket
"""

import os
from typing import Dict, List, Optional, Union
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.constants import POLYGON
from decimal import Decimal
import time


class PolymarketBot:
    """
    A trading bot for Polymarket that provides core functionality:
    - Portfolio value checking
    - Cash balance checking
    - Buying positions
    - Selling positions
    """
    
    def __init__(self, private_key: str, chain_id: int = POLYGON, testnet: bool = False):
        """
        Initialize the Polymarket trading bot.
        
        Args:
            private_key: Ethereum private key for authentication
            chain_id: Chain ID (default: POLYGON for mainnet)
            testnet: Whether to use testnet (default: False)
        """
        self.private_key = private_key
        self.chain_id = chain_id
        
        # Initialize the CLOB client
        host = "https://clob.polymarket.com" if not testnet else "https://clob-testnet.polymarket.com"
        self.client = ClobClient(
            host=host,
            key=private_key,
            chain_id=chain_id
        )
        
        # Get the wallet address
        self.address = self.client.get_address()
        print(f"Initialized Polymarket Bot for address: {self.address}")
    
    def get_portfolio_value(self) -> Dict[str, Union[float, List[Dict]]]:
        """
        Get the total portfolio value including cash and positions.
        
        Returns:
            Dictionary containing:
                - total_value: Total portfolio value in USD
                - cash_balance: Available cash balance
                - positions: List of open positions with their values
                - positions_value: Total value of all positions
        """
        try:
            # Get cash balance
            cash_balance = self.get_cash_balance()
            
            # Get open positions
            positions = self.client.get_positions(self.address)
            
            # Calculate positions value
            positions_value = 0.0
            position_details = []
            
            for position in positions:
                # Get current market price for the position
                token_id = position.get('asset_id', '')
                size = float(position.get('size', 0))
                
                # Skip if no size
                if size == 0:
                    continue
                
                # Get order book to find current price
                try:
                    orderbook = self.client.get_order_book(token_id)
                    
                    # Use mid price (average of best bid and ask)
                    best_bid = float(orderbook.get('bids', [{'price': 0}])[0].get('price', 0)) if orderbook.get('bids') else 0
                    best_ask = float(orderbook.get('asks', [{'price': 0}])[0].get('price', 0)) if orderbook.get('asks') else 0
                    
                    if best_bid > 0 and best_ask > 0:
                        mid_price = (best_bid + best_ask) / 2
                    elif best_bid > 0:
                        mid_price = best_bid
                    elif best_ask > 0:
                        mid_price = best_ask
                    else:
                        mid_price = 0
                    
                    position_value = size * mid_price
                    positions_value += position_value
                    
                    position_details.append({
                        'token_id': token_id,
                        'size': size,
                        'current_price': mid_price,
                        'value': position_value,
                        'market': position.get('market', 'Unknown')
                    })
                    
                except Exception as e:
                    print(f"Warning: Could not get price for token {token_id}: {e}")
                    position_details.append({
                        'token_id': token_id,
                        'size': size,
                        'current_price': None,
                        'value': None,
                        'market': position.get('market', 'Unknown')
                    })
            
            total_value = cash_balance + positions_value
            
            return {
                'total_value': total_value,
                'cash_balance': cash_balance,
                'positions_value': positions_value,
                'positions': position_details,
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"Error getting portfolio value: {e}")
            raise
    
    def get_cash_balance(self) -> float:
        """
        Get the available cash balance in the account.
        
        Returns:
            Available cash balance in USD
        """
        try:
            balance = self.client.get_balance_allowance()
            # The balance is returned as a string in wei-like format
            cash = float(balance.get('balance', 0)) / 1e6  # Convert from USDC format
            return cash
        except Exception as e:
            print(f"Error getting cash balance: {e}")
            raise
    
    def buy(
        self,
        token_id: str,
        amount: float,
        price: float,
        order_type: str = "GTC"
    ) -> Dict:
        """
        Place a buy order for a specific token.
        
        Args:
            token_id: The token ID to buy
            amount: The amount of tokens to buy
            price: The price per token (between 0 and 1)
            order_type: Order type (default: "GTC" - Good Till Cancelled)
                       Options: "GTC", "FOK" (Fill or Kill), "GTD" (Good Till Date)
        
        Returns:
            Order details including order ID
        """
        try:
            # Validate inputs
            if price <= 0 or price >= 1:
                raise ValueError("Price must be between 0 and 1")
            
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
            
            # Create order arguments
            order_args = OrderArgs(
                token_id=token_id,
                price=price,
                size=amount,
                side="BUY",
                order_type=OrderType[order_type]
            )
            
            # Place the order
            signed_order = self.client.create_order(order_args)
            order_result = self.client.post_order(signed_order)
            
            print(f"Buy order placed successfully!")
            print(f"Order ID: {order_result.get('orderID')}")
            print(f"Token: {token_id}")
            print(f"Amount: {amount}")
            print(f"Price: {price}")
            
            return {
                'success': True,
                'order_id': order_result.get('orderID'),
                'token_id': token_id,
                'amount': amount,
                'price': price,
                'side': 'BUY',
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"Error placing buy order: {e}")
            raise
    
    def sell(
        self,
        token_id: str,
        amount: float,
        price: float,
        order_type: str = "GTC"
    ) -> Dict:
        """
        Place a sell order for a specific token.
        
        Args:
            token_id: The token ID to sell
            amount: The amount of tokens to sell
            price: The price per token (between 0 and 1)
            order_type: Order type (default: "GTC" - Good Till Cancelled)
                       Options: "GTC", "FOK" (Fill or Kill), "GTD" (Good Till Date)
        
        Returns:
            Order details including order ID
        """
        try:
            # Validate inputs
            if price <= 0 or price >= 1:
                raise ValueError("Price must be between 0 and 1")
            
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
            
            # Create order arguments
            order_args = OrderArgs(
                token_id=token_id,
                price=price,
                size=amount,
                side="SELL",
                order_type=OrderType[order_type]
            )
            
            # Place the order
            signed_order = self.client.create_order(order_args)
            order_result = self.client.post_order(signed_order)
            
            print(f"Sell order placed successfully!")
            print(f"Order ID: {order_result.get('orderID')}")
            print(f"Token: {token_id}")
            print(f"Amount: {amount}")
            print(f"Price: {price}")
            
            return {
                'success': True,
                'order_id': order_result.get('orderID'),
                'token_id': token_id,
                'amount': amount,
                'price': price,
                'side': 'SELL',
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"Error placing sell order: {e}")
            raise
    
    def get_open_orders(self) -> List[Dict]:
        """
        Get all open orders for the account.
        
        Returns:
            List of open orders
        """
        try:
            orders = self.client.get_orders()
            return orders
        except Exception as e:
            print(f"Error getting open orders: {e}")
            raise
    
    def cancel_order(self, order_id: str) -> Dict:
        """
        Cancel a specific order.
        
        Args:
            order_id: The order ID to cancel
        
        Returns:
            Cancellation result
        """
        try:
            result = self.client.cancel_order(order_id)
            print(f"Order {order_id} cancelled successfully")
            return result
        except Exception as e:
            print(f"Error cancelling order: {e}")
            raise
    
    def get_markets(self, limit: int = 10) -> List[Dict]:
        """
        Get available markets on Polymarket.
        
        Args:
            limit: Maximum number of markets to return
        
        Returns:
            List of markets
        """
        try:
            markets = self.client.get_markets(limit=limit)
            return markets
        except Exception as e:
            print(f"Error getting markets: {e}")
            raise
    
    def get_market_info(self, condition_id: str) -> Dict:
        """
        Get detailed information about a specific market.
        
        Args:
            condition_id: The condition ID of the market
        
        Returns:
            Market details
        """
        try:
            market = self.client.get_market(condition_id)
            return market
        except Exception as e:
            print(f"Error getting market info: {e}")
            raise


def main():
    """
    Example usage of the Polymarket trading bot.
    """
    # Get private key from environment variable
    private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
    
    if not private_key:
        print("Error: POLYMARKET_PRIVATE_KEY environment variable not set")
        print("Please set your Ethereum private key as an environment variable:")
        print("export POLYMARKET_PRIVATE_KEY='your_private_key_here'")
        return
    
    # Initialize the bot
    bot = PolymarketBot(private_key)
    
    # Example: Check portfolio value
    print("\n=== Portfolio Value ===")
    portfolio = bot.get_portfolio_value()
    print(f"Total Value: ${portfolio['total_value']:.2f}")
    print(f"Cash Balance: ${portfolio['cash_balance']:.2f}")
    print(f"Positions Value: ${portfolio['positions_value']:.2f}")
    
    if portfolio['positions']:
        print("\nPositions:")
        for pos in portfolio['positions']:
            print(f"  - {pos['market']}: {pos['size']} tokens @ ${pos['current_price']:.4f} = ${pos['value']:.2f}")
    
    # Example: Check cash balance
    print("\n=== Cash Balance ===")
    cash = bot.get_cash_balance()
    print(f"Available Cash: ${cash:.2f}")
    
    # Example: Get markets
    print("\n=== Available Markets (Top 5) ===")
    markets = bot.get_markets(limit=5)
    for i, market in enumerate(markets, 1):
        print(f"{i}. {market.get('question', 'Unknown')}")
    
    # Note: Uncomment the following to place actual orders
    # Example: Buy
    # print("\n=== Placing Buy Order ===")
    # result = bot.buy(
    #     token_id="<token_id_here>",
    #     amount=10,
    #     price=0.5
    # )
    
    # Example: Sell
    # print("\n=== Placing Sell Order ===")
    # result = bot.sell(
    #     token_id="<token_id_here>",
    #     amount=5,
    #     price=0.6
    # )


if __name__ == "__main__":
    main()
