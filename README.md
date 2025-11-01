# Polymarket Trading Bot

A foundational trading bot for Polymarket that provides core functionality for automated trading operations.

## Features

The bot currently supports:

1. **Check Portfolio Value** - View your total portfolio value and positions
2. **Check Cash Value** - Check available USDC balance
3. **Buy** - Place buy orders on Polymarket markets
4. **Sell** - Place sell orders on Polymarket markets

## Setup

### Prerequisites

- Python 3.8 or higher
- Polymarket API key

### Installation

1. Clone this repository or navigate to the project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your Polymarket API key:

   Option 1: Set as environment variable
   ```bash
   export POLYMARKET_API_KEY="your_api_key_here"
   ```

   Option 2: Create a `.env` file (you'll need python-dotenv package):
   ```bash
   POLYMARKET_API_KEY=your_api_key_here
   ```

   Option 3: Pass directly when initializing:
   ```python
   trader = PolymarketTrader(api_key="your_api_key_here")
   ```

## Usage

### Basic Example

```python
from decimal import Decimal
from polymarket_trader import PolymarketTrader

# Initialize the trader
trader = PolymarketTrader(api_key="your_api_key_here")

# Check cash balance
cash_info = trader.get_cash_value()
print(f"Cash Balance: {cash_info['cash_balance']} {cash_info['currency']}")

# Check portfolio
portfolio_info = trader.get_portfolio_value()
print(f"Total Portfolio Value: {portfolio_info['total_value']}")

# Place a buy order
buy_result = trader.buy(
    condition_id="0x1234...",  # Market condition ID
    outcome="YES",
    amount=Decimal("1"),
    price=Decimal("0.5")
)

# Place a sell order
sell_result = trader.sell(
    condition_id="0x1234...",  # Market condition ID
    outcome="YES",
    amount=Decimal("1"),
    price=Decimal("0.5")
)
```

### Run Example Script

```bash
python example_usage.py
```

## API Reference

### `PolymarketTrader(api_key: Optional[str] = None)`

Initialize the trading bot.

- `api_key`: Polymarket API key (optional if set in environment)

### `get_portfolio_value() -> Dict[str, Any]`

Get total portfolio value and positions.

Returns:
- `total_value`: Total portfolio value (Decimal)
- `positions`: List of position dictionaries
- `raw_data`: Raw API response

### `get_cash_value() -> Dict[str, Any]`

Get available USDC balance.

Returns:
- `cash_balance`: Available USDC (Decimal)
- `currency`: Currency code ("USDC")

### `buy(condition_id: str, outcome: str, amount: Decimal, price: Optional[Decimal] = None) -> Dict[str, Any]`

Place a buy order.

Parameters:
- `condition_id`: Market condition ID
- `outcome`: Outcome to buy ("YES" or "NO")
- `amount`: Amount to buy in shares
- `price`: Price per share (optional, will use market price if not provided)

Returns:
- Order information dictionary

### `sell(condition_id: str, outcome: str, amount: Decimal, price: Optional[Decimal] = None) -> Dict[str, Any]`

Place a sell order.

Parameters:
- `condition_id`: Market condition ID
- `outcome`: Outcome to sell ("YES" or "NO")
- `amount`: Amount to sell in shares
- `price`: Price per share (optional, will use market price if not provided)

Returns:
- Order information dictionary

## Notes

- This is a foundational/proof-of-concept implementation
- API endpoints may need adjustment based on Polymarket's actual API structure
- Always test with small amounts first
- Make sure to handle errors appropriately in production use
- Market price fetching needs implementation of order book parsing for accurate prices

## Future Enhancements

- Order book parsing for accurate market prices
- Order status checking
- Order cancellation
- Advanced order types (stop-loss, take-profit)
- Portfolio analytics and tracking
- Risk management features
- Automated trading strategies
