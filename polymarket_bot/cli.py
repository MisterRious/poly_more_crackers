from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from rich.console import Console
from rich.table import Table

from .config import get_settings
from .client import PolymarketTradingClient


console = Console()


def _print_balances(balances: Any) -> None:
    table = Table(title="Balances")
    table.add_column("Asset")
    table.add_column("Available", justify="right")
    table.add_column("Total", justify="right")

    # Attempt a few common shapes
    if isinstance(balances, dict) and "balances" in balances and isinstance(balances["balances"], list):
        items = balances["balances"]
    elif isinstance(balances, list):
        items = balances
    elif isinstance(balances, dict):
        # fallback: dict of asset->amount
        for k, v in balances.items():
            table.add_row(str(k), str(v), str(v))
        console.print(table)
        return
    else:
        console.print_json(data=balances)
        return

    for b in items:
        asset = str(b.get("asset") or b.get("symbol") or b.get("token") or b.get("currency") or "?")
        available = b.get("available") or b.get("free") or b.get("balance") or b.get("amount") or 0
        total = b.get("total") or b.get("balance") or available or 0
        table.add_row(asset, str(available), str(total))

    console.print(table)


def _print_positions(positions: Any, portfolio_value: float | None) -> None:
    table = Table(title="Positions")
    table.add_column("Token/Outcome")
    table.add_column("Qty", justify="right")
    table.add_column("Est. Px", justify="right")
    table.add_column("Est. Value", justify="right")

    if not isinstance(positions, list):
        console.print_json(data=positions)
        return

    total_value = 0.0
    for p in positions:
        token = p.get("token_id") or p.get("tokenId") or p.get("asset") or p.get("asset_id") or "?"
        qty = p.get("qty") or p.get("quantity") or p.get("size") or p.get("amount") or 0
        # optional: if the API includes a mark/price
        est_px = p.get("markPrice") or p.get("price") or None
        try:
            qty_f = float(qty)
        except Exception:
            qty_f = 0.0
        try:
            est_px_f = float(est_px) if est_px is not None else None
        except Exception:
            est_px_f = None
        est_val = qty_f * est_px_f if (est_px_f is not None) else None
        total_value += est_val or 0.0
        table.add_row(str(token), f"{qty_f:.4f}", "-" if est_px_f is None else f"{est_px_f:.4f}", "-" if est_val is None else f"{est_val:.2f}")

    console.print(table)
    if portfolio_value is not None:
        console.print(f"[bold]Estimated portfolio value:[/bold] {portfolio_value:.2f}")
    else:
        console.print("[bold]Estimated portfolio value:[/bold] N/A (insufficient market data)")


def cmd_cash(args: argparse.Namespace) -> int:
    settings = get_settings()
    client = PolymarketTradingClient(settings.api_key, settings.private_key, settings.host)
    balances = client.get_balances()
    _print_balances(balances)
    return 0


def cmd_portfolio(args: argparse.Namespace) -> int:
    settings = get_settings()
    client = PolymarketTradingClient(settings.api_key, settings.private_key, settings.host)
    positions = client.get_positions()
    est_total = client.estimate_portfolio_value()
    _print_positions(positions, est_total)
    return 0


def cmd_buy(args: argparse.Namespace) -> int:
    settings = get_settings()
    client = PolymarketTradingClient(settings.api_key, settings.private_key, settings.host)
    if settings.dry_run:
        console.print("[yellow]DRY RUN[/yellow]: buy", args)
        return 0
    resp = client.place_order(
        token_id=args.token_id,
        market_id=args.market_id,
        outcome=args.outcome,
        side="BUY",
        price=args.price,
        size=args.size,
        time_in_force=args.tif,
        post_only=args.post_only,
    )
    console.print_json(data={"order_id": resp.order_id, "status": resp.status, "raw": resp.raw})
    return 0


def cmd_sell(args: argparse.Namespace) -> int:
    settings = get_settings()
    client = PolymarketTradingClient(settings.api_key, settings.private_key, settings.host)
    if settings.dry_run:
        console.print("[yellow]DRY RUN[/yellow]: sell", args)
        return 0
    resp = client.place_order(
        token_id=args.token_id,
        market_id=args.market_id,
        outcome=args.outcome,
        side="SELL",
        price=args.price,
        size=args.size,
        time_in_force=args.tif,
        post_only=args.post_only,
    )
    console.print_json(data={"order_id": resp.order_id, "status": resp.status, "raw": resp.raw})
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="polymarket-bot", description="Polymarket trading MVP")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_cash = sub.add_parser("cash", help="Show cash/balances")
    p_cash.set_defaults(func=cmd_cash)

    p_port = sub.add_parser("portfolio", help="Show positions and estimated value")
    p_port.set_defaults(func=cmd_portfolio)

    order_common = argparse.ArgumentParser(add_help=False)
    order_common.add_argument("--token-id", help="Outcome token id", default=None)
    order_common.add_argument("--market-id", help="Market id (if supported)", default=None)
    order_common.add_argument("--outcome", help="Outcome label/index (if supported)", default=None)
    order_common.add_argument("--price", type=float, required=True, help="Limit price (0-1)")
    order_common.add_argument("--size", type=float, required=True, help="Order size (shares)")
    order_common.add_argument("--tif", default="GTC", help="Time in force e.g. GTC, IOC")
    order_common.add_argument("--post-only", action="store_true", help="Post-only order")

    p_buy = sub.add_parser("buy", parents=[order_common], help="Place a buy limit order")
    p_buy.set_defaults(func=cmd_buy)

    p_sell = sub.add_parser("sell", parents=[order_common], help="Place a sell limit order")
    p_sell.set_defaults(func=cmd_sell)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
