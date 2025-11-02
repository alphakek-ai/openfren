def test_fetch_market_sentiment_async_is_coroutine():
    import inspect

    from openfren.app import fetch_market_sentiment_async  # type: ignore[attr-defined]

    assert inspect.iscoroutinefunction(fetch_market_sentiment_async)


def test_timeout_constants_exist():
    from openfren.app import CONNECT_TIMEOUT_S, READ_TIMEOUT_S  # type: ignore[attr-defined]

    assert isinstance(CONNECT_TIMEOUT_S, (int, float))
    assert isinstance(READ_TIMEOUT_S, (int, float))
    assert CONNECT_TIMEOUT_S <= READ_TIMEOUT_S
