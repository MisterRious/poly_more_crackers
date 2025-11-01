"""
Example usage of the Polymarket Trading Bot.
Demonstrates how to use the core functions.
"""

from decimal import Decimal
from polymarket_trader import PolymarketTrader
import os


def main():
    """
    Example usage of the Polymarket trading bot.
    """
    # Initialize the trader with API key
    # Option 1: From environment variable
    # Make sure to set POLYMARKET_API_KEY in your environment
    api_key = os.getenv("POLYMARKET_API_KEY")
    
    if not api_key:
        print("Please set POLYMARKET_API_KEY environment variable")
        print("Or modify this script to pass the API key directly")
        return
    
    trader = PolymarketTrader(api_key=api_key)
    
    try:
        # 1. Check cash value
        print("\n=== Checking Cash Value ===")
        cash_info = trader.get_cash_value()
        print(f"Cash Balance: {cash_info['cash_balance']} {cash_info['currency']}")
        
        # 2. Check portfolio value
        print("\n=== Checking Portfolio Value ===")
        portfolio_info = trader.get_portfolio_value()
        print(f"Total Portfolio Value: {portfolio_info['total_value']}")
        print(f"Number of Positions: {len(portfolio_info['positions'])}")
        for position in portfolio_info['positions']:
            print(f"  - {position.get('token', 'N/A')}: {position.get('amount', 0)}")
        
        # 3. Buy example (commented out to prevent accidental trades)
        print("\n=== Buy Example (Commented Out) ===")
        print("# Example: trader.buy('condition_id', 'YES', Decimal('1'), Decimal('0.5'))")
        # Uncomment to place a real order:
        # buy_result = trader.buy(
        #     condition_id="0x1234...",  # Replace with actual condition ID
        #     outcome="YES",
        #     amount=Decimal("1"),
        #     price=Decimal("0.5")
        # )
        # print(f"Buy Order Result: {buy_result}")
        
        # 4. Sell example (commented out to prevent accidental trades)
        print("\n=== Sell Example (Commented Out) ===")
        print("# Example: trader.sell('condition_id', 'YES', Decimal('1'), Decimal('0.5'))")
        # Uncomment to place a real order:
        # sell_result = trader.sell(
        #     condition_id="0x1234...",  # Replace with actual condition ID
        #     outcome="YES",
        #     amount=Decimal("1"),
        #     price=Decimal("0.5")
        # )
        # print(f"Sell Order Result: {sell_result}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
