"""
Example usage scenarios for the Polymarket Trading Bot
"""

import os
from polymarket_bot import PolymarketBot
from dotenv import load_dotenv


def example_check_portfolio():
    """Example: Check portfolio and positions"""
    load_dotenv()
    private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
    
    bot = PolymarketBot(private_key)
    
    print("=" * 60)
    print("PORTFOLIO OVERVIEW")
    print("=" * 60)
    
    portfolio = bot.get_portfolio_value()
    
    print(f"\n?? Total Portfolio Value: ${portfolio['total_value']:.2f}")
    print(f"?? Cash Balance: ${portfolio['cash_balance']:.2f}")
    print(f"?? Positions Value: ${portfolio['positions_value']:.2f}")
    
    if portfolio['positions']:
        print(f"\n?? Open Positions ({len(portfolio['positions'])}):")
        print("-" * 60)
        for i, pos in enumerate(portfolio['positions'], 1):
            print(f"\n{i}. Market: {pos['market']}")
            print(f"   Token ID: {pos['token_id']}")
            print(f"   Size: {pos['size']} tokens")
            if pos['current_price'] is not None:
                print(f"   Current Price: ${pos['current_price']:.4f}")
                print(f"   Position Value: ${pos['value']:.2f}")
    else:
        print("\n?? No open positions")


def example_check_cash():
    """Example: Check available cash balance"""
    load_dotenv()
    private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
    
    bot = PolymarketBot(private_key)
    
    print("=" * 60)
    print("CASH BALANCE")
    print("=" * 60)
    
    cash = bot.get_cash_balance()
    print(f"\n?? Available Cash: ${cash:.2f}")
    
    if cash > 0:
        print(f"\n? You have funds available for trading!")
    else:
        print(f"\n??  No funds available. Please deposit USDC to your account.")


def example_browse_markets():
    """Example: Browse available markets"""
    load_dotenv()
    private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
    
    bot = PolymarketBot(private_key)
    
    print("=" * 60)
    print("AVAILABLE MARKETS")
    print("=" * 60)
    
    markets = bot.get_markets(limit=10)
    
    print(f"\n?? Top {len(markets)} Markets:\n")
    for i, market in enumerate(markets, 1):
        print(f"{i}. {market.get('question', 'Unknown')}")
        print(f"   Condition ID: {market.get('condition_id', 'N/A')}")
        print(f"   Active: {market.get('active', 'N/A')}")
        print()


def example_place_buy_order():
    """
    Example: Place a buy order
    
    WARNING: This example is commented out to prevent accidental trades.
    Uncomment and modify with real token IDs to place actual orders.
    """
    load_dotenv()
    private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
    
    bot = PolymarketBot(private_key)
    
    print("=" * 60)
    print("PLACE BUY ORDER (Example)")
    print("=" * 60)
    
    # UNCOMMENT AND MODIFY THE FOLLOWING TO PLACE A REAL ORDER:
    # 
    # token_id = "your_token_id_here"  # Token ID for the outcome you want to buy
    # amount = 10  # Number of shares to buy
    # price = 0.55  # Price per share (between 0 and 1)
    # 
    # print(f"\nPlacing buy order:")
    # print(f"  Token: {token_id}")
    # print(f"  Amount: {amount} shares")
    # print(f"  Price: ${price} per share")
    # print(f"  Total cost: ${amount * price}")
    # 
    # # Confirm before placing
    # confirm = input("\nConfirm order? (yes/no): ")
    # if confirm.lower() == 'yes':
    #     result = bot.buy(
    #         token_id=token_id,
    #         amount=amount,
    #         price=price
    #     )
    #     print(f"\n? Order placed! Order ID: {result['order_id']}")
    # else:
    #     print("\n? Order cancelled")
    
    print("\n??  This is an example only. Uncomment the code to place real orders.")


def example_place_sell_order():
    """
    Example: Place a sell order
    
    WARNING: This example is commented out to prevent accidental trades.
    Uncomment and modify with real token IDs to place actual orders.
    """
    load_dotenv()
    private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
    
    bot = PolymarketBot(private_key)
    
    print("=" * 60)
    print("PLACE SELL ORDER (Example)")
    print("=" * 60)
    
    # UNCOMMENT AND MODIFY THE FOLLOWING TO PLACE A REAL ORDER:
    # 
    # token_id = "your_token_id_here"  # Token ID for the outcome you want to sell
    # amount = 5  # Number of shares to sell
    # price = 0.65  # Price per share (between 0 and 1)
    # 
    # print(f"\nPlacing sell order:")
    # print(f"  Token: {token_id}")
    # print(f"  Amount: {amount} shares")
    # print(f"  Price: ${price} per share")
    # print(f"  Total value: ${amount * price}")
    # 
    # # Confirm before placing
    # confirm = input("\nConfirm order? (yes/no): ")
    # if confirm.lower() == 'yes':
    #     result = bot.sell(
    #         token_id=token_id,
    #         amount=amount,
    #         price=price
    #     )
    #     print(f"\n? Order placed! Order ID: {result['order_id']}")
    # else:
    #     print("\n? Order cancelled")
    
    print("\n??  This is an example only. Uncomment the code to place real orders.")


def example_check_orders():
    """Example: Check open orders"""
    load_dotenv()
    private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
    
    bot = PolymarketBot(private_key)
    
    print("=" * 60)
    print("OPEN ORDERS")
    print("=" * 60)
    
    orders = bot.get_open_orders()
    
    if orders:
        print(f"\n?? You have {len(orders)} open order(s):\n")
        for i, order in enumerate(orders, 1):
            print(f"{i}. Order ID: {order.get('id', 'N/A')}")
            print(f"   Side: {order.get('side', 'N/A')}")
            print(f"   Size: {order.get('size', 'N/A')}")
            print(f"   Price: ${order.get('price', 'N/A')}")
            print()
    else:
        print("\n?? No open orders")


def main():
    """Run all examples"""
    if not os.getenv("POLYMARKET_PRIVATE_KEY"):
        print("??  Error: POLYMARKET_PRIVATE_KEY not set!")
        print("\nPlease set your private key in one of these ways:")
        print("1. Create a .env file with POLYMARKET_PRIVATE_KEY=your_key")
        print("2. Export the environment variable: export POLYMARKET_PRIVATE_KEY=your_key")
        return
    
    print("\n?? Polymarket Trading Bot - Examples\n")
    
    while True:
        print("\n" + "=" * 60)
        print("MAIN MENU")
        print("=" * 60)
        print("\n1. Check Portfolio Value")
        print("2. Check Cash Balance")
        print("3. Browse Available Markets")
        print("4. Place Buy Order (Example)")
        print("5. Place Sell Order (Example)")
        print("6. Check Open Orders")
        print("7. Exit")
        
        choice = input("\nSelect an option (1-7): ").strip()
        
        try:
            if choice == "1":
                example_check_portfolio()
            elif choice == "2":
                example_check_cash()
            elif choice == "3":
                example_browse_markets()
            elif choice == "4":
                example_place_buy_order()
            elif choice == "5":
                example_place_sell_order()
            elif choice == "6":
                example_check_orders()
            elif choice == "7":
                print("\n?? Goodbye!")
                break
            else:
                print("\n? Invalid option. Please select 1-7.")
        except Exception as e:
            print(f"\n? Error: {e}")
            print("Please check your configuration and try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
