## Polymarket Trading Bot (MVP)

Foundational Python code to interact with Polymarket's CLOB for:

- Check portfolio value
- Check cash value
- Buy
- Sell

This is a minimal proof-of-concept suitable for extension into an automated bot.

### Setup

1) Python 3.10+
2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Configure environment variables. Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

Required:

- `POLYMARKET_API_KEY`: Your Polymarket API key
- `POLYMARKET_PRIVATE_KEY`: Your wallet private key (0x?)

Optional:

- `POLYMARKET_HOST` (default `https://clob.polymarket.com`)
- `DRY_RUN` (`true`/`false`, default `false`)

### Usage

Run via the provided entrypoint:

```bash
python main.py cash
python main.py portfolio
python main.py buy --token-id <TOKEN_ID> --price 0.45 --size 10
python main.py sell --token-id <TOKEN_ID> --price 0.55 --size 5
```

Alternatively as a module:

```bash
python -m polymarket_bot.cli cash
```

Notes:

- For `buy`/`sell`, you can optionally pass `--market-id` and `--outcome` instead of `--token-id` if supported by your client version.
- Set `DRY_RUN=true` to print orders without submitting.

### Implementation

- `polymarket_bot/config.py`: Loads environment and settings
- `polymarket_bot/client.py`: Wrapper around `py-clob-client` with defensive method resolution
- `polymarket_bot/cli.py`: CLI commands for cash, portfolio, buy, sell
- `requirements.txt`: Dependencies (`py-clob-client`, `python-dotenv`, `requests`, `rich`)

### Extending

- Add strategy modules for automated execution (scheduling, risk, logging)
- Persistence and metrics (SQLite/PG + Prometheus/Grafana)
- Robust valuation using consistent market data source
- Order management (replace, cancel-on-disconnect, OCO)
