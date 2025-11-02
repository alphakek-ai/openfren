def test_sentiment_state_shape_and_types():
    from openfren import SentimentLabel, SentimentState  # type: ignore[attr-defined]

    state = SentimentState(label=SentimentLabel.NEUTRAL, score=5.0)
    assert state.label.value in {"bullish", "neutral", "bearish"}
    assert isinstance(state.score, float)


def test_sentiment_state_keeps_label_verbatim():
    from openfren import SentimentLabel, SentimentState  # type: ignore[attr-defined]

    state = SentimentState(label=SentimentLabel.BULLISH, score=7)
    assert state.label.value == "bullish"
    assert float(state.score) == 7.0
