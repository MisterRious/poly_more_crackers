# Polymarket Trading Bot

A foundational Python trading bot for [Polymarket](https://polymarket.com/) that provides core functionality for automated trading on prediction markets.

## Features

This MVP implementation includes the following core features:

1. ? **Check Portfolio Value** - View total portfolio value including cash and positions
2. ? **Check Cash Balance** - View available USDC balance
3. ? **Buy** - Place buy orders for market positions
4. ? **Sell** - Place sell orders for market positions

### Additional Features

- View open positions with current values
- Browse available markets
- Check and cancel open orders
- Support for different order types (GTC, FOK, GTD)

## Setup

### Prerequisites

- Python 3.8 or higher
- An Ethereum wallet with a private key
- USDC deposited in your Polymarket account

### Installation

1. Clone this repository or download the files

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your private key:

Create a `.env` file in the project directory:
```bash
cp .env.example .env
```

Edit `.env` and add your Ethereum private key:
```
POLYMARKET_PRIVATE_KEY=your_private_key_here
```

?? **IMPORTANT**: Never commit your `.env` file or share your private key!

## Usage

### Basic Usage

The main bot class is `PolymarketBot` in `polymarket_bot.py`. Here's a simple example:

```python
from polymarket_bot import PolymarketBot
import os

# Initialize the bot
bot = PolymarketBot(os.getenv("POLYMARKET_PRIVATE_KEY"))

# Check portfolio value
portfolio = bot.get_portfolio_value()
print(f"Total Value: ${portfolio['total_value']:.2f}")

# Check cash balance
cash = bot.get_cash_balance()
print(f"Cash: ${cash:.2f}")

# Place a buy order
result = bot.buy(
    token_id="your_token_id",
    amount=10,
    price=0.55
)

# Place a sell order
result = bot.sell(
    token_id="your_token_id",
    amount=5,
    price=0.65
)
```

### Interactive Examples

Run the example script with an interactive menu:

```bash
python example_usage.py
```

This provides a user-friendly interface to:
- Check your portfolio and positions
- View available markets
- See open orders
- Examples of placing buy/sell orders

### Running the Main Script

```bash
python polymarket_bot.py
```

This will display your current portfolio status and available markets.

## API Reference

### PolymarketBot Class

#### Initialization

```python
bot = PolymarketBot(private_key, chain_id=POLYGON, testnet=False)
```

**Parameters:**
- `private_key` (str): Your Ethereum private key
- `chain_id` (int): Blockchain chain ID (default: POLYGON for mainnet)
- `testnet` (bool): Use testnet instead of mainnet (default: False)

#### Methods

##### `get_portfolio_value() -> Dict`

Returns comprehensive portfolio information including total value, cash balance, and all positions.

**Returns:**
```python
{
    'total_value': float,        # Total portfolio value in USD
    'cash_balance': float,       # Available cash
    'positions_value': float,    # Total value of positions
    'positions': List[Dict],     # List of position details
    'timestamp': float           # Unix timestamp
}
```

##### `get_cash_balance() -> float`

Returns the available USDC balance.

**Returns:** Cash balance in USD

##### `buy(token_id: str, amount: float, price: float, order_type: str = "GTC") -> Dict`

Places a buy order for a specific outcome token.

**Parameters:**
- `token_id` (str): The token ID to buy
- `amount` (float): Number of shares to buy
- `price` (float): Price per share (between 0 and 1)
- `order_type` (str): Order type - "GTC", "FOK", or "GTD"

**Returns:**
```python
{
    'success': bool,
    'order_id': str,
    'token_id': str,
    'amount': float,
    'price': float,
    'side': str,
    'timestamp': float
}
```

##### `sell(token_id: str, amount: float, price: float, order_type: str = "GTC") -> Dict`

Places a sell order for a specific outcome token.

**Parameters:** Same as `buy()`

**Returns:** Same structure as `buy()`

##### `get_open_orders() -> List[Dict]`

Returns all open orders for the account.

##### `cancel_order(order_id: str) -> Dict`

Cancels a specific order by ID.

##### `get_markets(limit: int = 10) -> List[Dict]`

Returns available markets on Polymarket.

##### `get_market_info(condition_id: str) -> Dict`

Returns detailed information about a specific market.

## Project Structure

```
polymarket-trading-bot/
??? polymarket_bot.py      # Main bot class with core functionality
??? example_usage.py       # Interactive examples and usage scenarios
??? requirements.txt       # Python dependencies
??? .env.example          # Example environment configuration
??? .env                  # Your private configuration (DO NOT COMMIT)
??? README.md            # This file
```

## Order Types

- **GTC (Good Till Cancelled)**: Order remains active until filled or manually cancelled
- **FOK (Fill or Kill)**: Order must be filled immediately in its entirety or cancelled
- **GTD (Good Till Date)**: Order remains active until a specific date/time

## Security Notes

?? **CRITICAL SECURITY INFORMATION**:

1. **Never share your private key** - It provides full access to your funds
2. **Never commit your `.env` file** - Add it to `.gitignore`
3. **Use environment variables** - Don't hardcode sensitive data
4. **Test with small amounts first** - Verify everything works before large trades
5. **Consider using a dedicated trading wallet** - Separate from your main holdings

## Limitations & Future Enhancements

This is a foundational MVP. Potential enhancements for automated trading:

- [ ] Automated trading strategies (e.g., market making, arbitrage)
- [ ] Real-time market monitoring and alerts
- [ ] Risk management and position sizing
- [ ] Historical data analysis and backtesting
- [ ] Multi-market portfolio optimization
- [ ] Webhook/API server for remote control
- [ ] Docker containerization for cloud deployment
- [ ] Logging and performance tracking
- [ ] Stop-loss and take-profit automation

## Troubleshooting

### "POLYMARKET_PRIVATE_KEY not set"

Make sure you've created a `.env` file with your private key or exported it as an environment variable:

```bash
export POLYMARKET_PRIVATE_KEY='your_private_key_here'
```

### "Insufficient balance"

Ensure you have USDC deposited in your Polymarket account. You can deposit through the Polymarket website.

### Import errors

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Connection errors

Check your internet connection and verify that Polymarket's API is accessible.

## Resources

- [Polymarket Website](https://polymarket.com/)
- [Polymarket CLOB Client Documentation](https://github.com/Polymarket/py-clob-client)
- [Polymarket API Documentation](https://docs.polymarket.com/)

## Disclaimer

This software is provided for educational purposes only. Trading on prediction markets involves financial risk. Always do your own research and never trade more than you can afford to lose. The authors are not responsible for any financial losses incurred while using this software.

## License

MIT License - Feel free to use and modify as needed.

---

**Ready to trade?** Make sure you've set up your private key and have USDC in your account, then start with `python example_usage.py` to explore the features!
