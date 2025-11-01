import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    api_key: str
    private_key: str
    host: str = os.getenv("POLYMARKET_HOST", "https://clob.polymarket.com")
    dry_run: bool = os.getenv("DRY_RUN", "false").lower() in {"1", "true", "yes"}


def get_settings() -> Settings:
    api_key = os.getenv("POLYMARKET_API_KEY", "").strip()
    private_key = os.getenv("POLYMARKET_PRIVATE_KEY", "").strip()
    host = os.getenv("POLYMARKET_HOST", "https://clob.polymarket.com").strip()
    dry_run = os.getenv("DRY_RUN", "false").lower() in {"1", "true", "yes"}

    if not api_key:
        raise RuntimeError("POLYMARKET_API_KEY is not set")
    if not private_key:
        raise RuntimeError("POLYMARKET_PRIVATE_KEY is not set")

    return Settings(api_key=api_key, private_key=private_key, host=host, dry_run=dry_run)
