def test_public_api_imports():
    from openfren import (
        CONNECT_TIMEOUT_S,
        READ_TIMEOUT_S,
        SENTIMENT_SOUNDS,
        SentimentLabel,
        SentimentState,
        fetch_market_sentiment_async,
        label_from_score,
    )  # type: ignore[attr-defined]

    assert isinstance(CONNECT_TIMEOUT_S, (int, float))
    assert isinstance(READ_TIMEOUT_S, (int, float))
    assert callable(label_from_score)
    assert callable(fetch_market_sentiment_async)
    assert set(SENTIMENT_SOUNDS.keys()) == {
        SentimentLabel.BULLISH,
        SentimentLabel.NEUTRAL,
        SentimentLabel.BEARISH,
    }


