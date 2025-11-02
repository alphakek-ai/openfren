"""Openfren public API.

This package exposes a small, stable surface for consumers:
- SentimentLabel: enumeration of sentiment labels
- label_from_score(score): convert numeric score to label
- SentimentState: pydantic model for shared state
- fetch_market_sentiment_async(...): async HTTP fetcher returning (label, score)
"""

from .app import (
    CONNECT_TIMEOUT_S,
    READ_TIMEOUT_S,
    SENTIMENT_SOUNDS,
    SentimentLabel,
    SentimentState,
    fetch_market_sentiment_async,
    label_from_score,
)

__all__ = [
    "CONNECT_TIMEOUT_S",
    "READ_TIMEOUT_S",
    "SENTIMENT_SOUNDS",
    "SentimentLabel",
    "SentimentState",
    "fetch_market_sentiment_async",
    "label_from_score",
]
