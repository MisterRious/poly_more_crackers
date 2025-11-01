"""
Configuration file for Polymarket Trading Bot.
Handles API key management and configuration settings.
"""

import os
from typing import Optional


def get_api_key() -> Optional[str]:
    """
    Get the Polymarket API key from environment variable.
    
    Returns:
        API key string or None if not found
    """
    return os.getenv("POLYMARKET_API_KEY")


def set_api_key(api_key: str) -> None:
    """
    Set the Polymarket API key as an environment variable.
    Note: This only sets it for the current process.
    For persistence, set POLYMARKET_API_KEY in your environment.
    
    Args:
        api_key: The Polymarket API key
    """
    os.environ["POLYMARKET_API_KEY"] = api_key
