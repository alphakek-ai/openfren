def test_label_from_score_boundaries_and_clamping():
    from openfren import SentimentLabel, label_from_score  # type: ignore[attr-defined]

    # Lower bound clamp
    assert label_from_score(-100) is SentimentLabel.BEARISH
    assert label_from_score(0) is SentimentLabel.BEARISH

    # Boundary transitions
    assert label_from_score(1) is SentimentLabel.BEARISH
    assert label_from_score(3) is SentimentLabel.BEARISH
    assert label_from_score(4) is SentimentLabel.NEUTRAL
    assert label_from_score(7) is SentimentLabel.NEUTRAL
    assert label_from_score(8) is SentimentLabel.BULLISH
    assert label_from_score(10) is SentimentLabel.BULLISH

    # Upper bound clamp
    assert label_from_score(11) is SentimentLabel.BULLISH
    assert label_from_score(1000) is SentimentLabel.BULLISH
