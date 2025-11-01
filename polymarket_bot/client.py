from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class OrderResponse:
    order_id: str
    status: str
    raw: dict


class PolymarketTradingClient:
    """Lightweight wrapper over the official py-clob-client with graceful fallbacks.

    This wrapper attempts multiple known method/constructor signatures to reduce
    coupling to upstream changes.
    """

    def __init__(self, api_key: str, private_key: str, host: str) -> None:
        self._raw_client = self._init_underlying_client(api_key, private_key, host)

    def _init_underlying_client(self, api_key: str, private_key: str, host: str):
        try:
            from py_clob_client.client import ClobClient  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "py-clob-client is required. Install with `pip install py-clob-client`."
            ) from exc

        # Try a few known constructor signatures
        last_err: Optional[Exception] = None
        for kwargs in (
            {"api_key": api_key, "private_key": private_key, "host": host},
            {"api_key": api_key, "private_key": private_key, "base_url": host},
            {"api_key": api_key, "private_key": private_key, "api_url": host},
        ):
            try:
                return ClobClient(**kwargs)
            except TypeError as e:
                last_err = e
                continue
        # If none worked, raise the last error
        raise RuntimeError(f"Could not initialize ClobClient with provided host: {host}") from last_err

    # --- Low-level passthrough helpers
    def _call(self, names: List[str], *args, **kwargs):
        for name in names:
            meth = getattr(self._raw_client, name, None)
            if callable(meth):
                return meth(*args, **kwargs)
        raise AttributeError(f"None of methods {names} found on underlying client")

    # --- Balances & positions
    def get_balances(self) -> Dict[str, Any]:
        return self._call(["get_balances", "balances" ])

    def get_positions(self) -> List[Dict[str, Any]]:
        return self._call(["get_positions", "positions" ])

    # --- Market data (best-effort helpers, may not exist depending on client version)
    def get_ticker(self, token_id: str) -> Optional[Dict[str, Any]]:
        try:
            return self._call(["get_ticker", "ticker"], token_id)
        except Exception:
            return None

    def get_orderbook(self, token_id: str) -> Optional[Dict[str, Any]]:
        try:
            return self._call(["get_orderbook", "orderbook"], token_id)
        except Exception:
            return None

    # --- Orders
    def place_order(
        self,
        *,
        token_id: Optional[str] = None,
        market_id: Optional[str] = None,
        outcome: Optional[str] = None,
        side: str,
        price: float,
        size: float,
        time_in_force: str = "GTC",
        post_only: bool = False,
    ) -> OrderResponse:
        payload: Dict[str, Any] = {
            "side": side.upper(),
            "price": float(price),
            "size": float(size),
            "time_in_force": time_in_force,
            "post_only": bool(post_only),
        }
        if token_id:
            payload["token_id"] = token_id
        if market_id:
            payload["market_id"] = market_id
        if outcome:
            payload["outcome"] = outcome

        raw = self._call(["place_order", "post_order", "create_order", "order"], payload)
        order_id = raw.get("orderId") or raw.get("id") or raw.get("order_id") or ""
        status = raw.get("status") or "submitted"
        return OrderResponse(order_id=order_id, status=status, raw=raw)

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        return self._call(["cancel_order", "cancel"], order_id)

    # --- Convenience valuations (best-effort)
    def estimate_position_value(self, position: Dict[str, Any]) -> Optional[float]:
        """Estimate mark-to-market value for a single position if possible.

        Attempts to use ticker mid, then orderbook mid; falls back to None.
        Expects one of token_id/asset_id fields and a quantity/size/amount field.
        """
        token_id = (
            position.get("token_id")
            or position.get("tokenId")
            or position.get("asset")
            or position.get("asset_id")
        )
        if not token_id:
            return None

        qty = (
            position.get("qty")
            or position.get("quantity")
            or position.get("size")
            or position.get("amount")
        )
        try:
            qty = float(qty)
        except Exception:
            return None

        # Try ticker mid
        ticker = self.get_ticker(token_id)
        if ticker:
            bid = float(ticker.get("bid") or ticker.get("bestBid") or 0.0)
            ask = float(ticker.get("ask") or ticker.get("bestAsk") or 0.0)
            mid = (bid + ask) / 2 if (bid > 0 and ask > 0) else float(ticker.get("last") or 0.0)
            if mid > 0:
                return qty * mid

        # Try orderbook mid
        ob = self.get_orderbook(token_id)
        if ob and isinstance(ob, dict):
            bids = ob.get("bids") or []
            asks = ob.get("asks") or []
            best_bid = float(bids[0][0]) if bids and bids[0] else 0.0
            best_ask = float(asks[0][0]) if asks and asks[0] else 0.0
            if best_bid > 0 and best_ask > 0:
                return qty * (best_bid + best_ask) / 2

        return None

    def estimate_portfolio_value(self) -> Optional[float]:
        try:
            positions = self.get_positions()
        except Exception:
            return None
        total: float = 0.0
        had_any = False
        for p in positions or []:
            val = self.estimate_position_value(p)
            if val is not None:
                total += val
                had_any = True
        return total if had_any else None
