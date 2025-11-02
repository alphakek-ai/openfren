import asyncio
import logging
import os
import random
import time
import traceback
from enum import StrEnum
from typing import Any, TypeAlias

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field


# Load environment variables from a .env file if present.
load_dotenv(".env", override=False)


# Configuration constants
POLL_INTERVAL_SECONDS: int = 300
AIKEK_API_URL: str = "https://api.alphakek.ai/knowledge/ask"
MOVES_DATASET: str = "pollen-robotics/reachy-mini-emotions-library"

# Networking
CONNECT_TIMEOUT_S: float = 5.0
READ_TIMEOUT_S: float = 300.0

# Motion and timing constants
SOUND_INTERVAL_RANGE_S: tuple[float, float] = (20.0, 60.0)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(logging.StreamHandler())


class SentimentLabel(StrEnum):
    """Enumeration of supported sentiment labels."""

    BULLISH = "bullish"
    NEUTRAL = "neutral"
    BEARISH = "bearish"


def label_from_score(score: int) -> SentimentLabel:
    """Map numeric score to a sentiment label.

    Score is clamped to [1, 10]: 1..3 -> BEARISH, 4..7 -> NEUTRAL, 8..10 -> BULLISH.
    """
    s = max(1, min(10, int(score)))
    if s <= 3:
        return SentimentLabel.BEARISH
    if s >= 8:
        return SentimentLabel.BULLISH
    return SentimentLabel.NEUTRAL


async def fetch_market_sentiment_async(
    api_url: str,
    *,
    question: str | None = None,
    token: str | None = None,
) -> tuple[SentimentLabel, float]:
    """Fetch market sentiment over HTTP.

    Args:
        api_url: Endpoint URL to call.
        question: Optional question to send to the API. If not provided, uses
            AIKEK_QUESTION environment variable or a sensible default.
        token: Optional bearer token to use. If not provided, uses
            AIKEK_API_TOKEN from the environment.

    Returns:
        A tuple of (label, score[1..10]). On failure, returns (NEUTRAL, 0.0).
    """
    q = question or os.getenv("AIKEK_QUESTION", "crypto market sentiment now, one line")
    t = token or os.getenv("AIKEK_API_TOKEN", "")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {t}" if t else "",
        "Content-Type": "application/json",
    }
    payload = {
        "question": q,
    }

    timeout = httpx.Timeout(CONNECT_TIMEOUT_S, read=READ_TIMEOUT_S)
    backoff = 0.5
    attempts = 3
    for attempt in range(1, attempts + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(api_url, json=payload, headers=headers)
                resp.raise_for_status()
                data: dict[str, Any] = resp.json()
                logger.info(f"AIKEK API response: {data}")
                s = int(data.get("sentiment", 5))
                label = label_from_score(s)
                score = float(max(1, min(10, s)))
                return label, score
        except Exception:
            logger.error(f"Async fetch attempt {attempt} failed")
            logger.error(traceback.format_exc())
            if attempt < attempts:
                await asyncio.sleep(backoff)
                backoff *= 2
            else:
                break
    return SentimentLabel.NEUTRAL, 0.0


MoveName: TypeAlias = str
SoundName: TypeAlias = str

MOVE_MAP: dict[SentimentLabel, list[MoveName]] = {
    # Positive / excited / happy
    SentimentLabel.BULLISH: [
        "laughing1",
        "laughing2",
        "cheerful1",
        "enthusiastic1",
        "enthusiastic2",
        "success1",
        "success2",
        "proud1",
        "proud2",
        "proud3",
        "welcoming1",
        "welcoming2",
        "dance1",
        "dance2",
        "dance3",
        "amazed1",
        "relief1",
        "relief2",
        "helpful1",
        "helpful2",
        "grateful1",
        "serenity1",
    ],
    # Neutral / conversational / acknowledgment
    SentimentLabel.NEUTRAL: [
        "understanding1",
        "understanding2",
        "thoughtful1",
        "thoughtful2",
        "inquiring1",
        "inquiring2",
        "inquiring3",
        "attentive1",
        "attentive2",
        "curious1",
        "indifferent1",
        "uncertain1",
        "yes1",
        "no1",
        "oops1",
        "oops2",
        "incomprehensible2",
    ],
    # Negative / sad / angry / tired
    SentimentLabel.BEARISH: [
        "displeased1",
        "displeased2",
        "irritated1",
        "irritated2",
        "furious1",
        "rage1",
        "contempt1",
        "go_away1",
        "disgusted1",
        "sad1",
        "sad2",
        "no_sad1",
        "downcast1",
        "exhausted1",
        "tired1",
        "boredom1",
        "boredom2",
        "lost1",
        "lonely1",
        "anxiety1",
        "fear1",
        "scared1",
        "reprimand1",
        "reprimand2",
        "reprimand3",
        "confused1",
    ],
}

SENTIMENT_SOUNDS: dict[SentimentLabel, list[SoundName]] = {
    SentimentLabel.BULLISH: ["dance1.wav"],
    SentimentLabel.NEUTRAL: ["count.wav"],
    SentimentLabel.BEARISH: ["go_sleep.wav", "confused1.wav"],
}


class SentimentState(BaseModel):
    """Validated sentiment state shared across tasks."""

    label: SentimentLabel
    score: float = Field(ge=0.0, le=10.0)


async def _movement_loop_async(
    mini: Any,
    recorded_moves: Any,
    stop_event: asyncio.Event,
    sentiment_state: SentimentState,
) -> None:
    """Continuously play moves; sentiment affects which move gets played next."""
    last_label: SentimentLabel = SentimentLabel.NEUTRAL

    now = time.monotonic()
    next_sound_at = now + random.uniform(*SOUND_INTERVAL_RANGE_S)

    while not stop_event.is_set():
        now = time.monotonic()
        # Sentiment-based sound
        cur_label = sentiment_state.label
        if now >= next_sound_at:
            sound_choices = SENTIMENT_SOUNDS[cur_label]
            sound_file = random.choice(sound_choices)
            logger.info(f"Playing sound: {sound_file}")
            mini.media.play_sound(sound_file)
            next_sound_at = time.monotonic() + random.uniform(*SOUND_INTERVAL_RANGE_S)

        # Choose and obtain move: prefer label-specific moves, else fallback
        available_moves = MOVE_MAP[cur_label]
        move_name = random.choice(available_moves)
        move = recorded_moves.get(move_name)

        # Longer initial goto if label changed
        initial_goto = 2 if cur_label != last_label else 1
        last_label = cur_label

        if stop_event.is_set():
            break
        try:
            await mini.async_play_move(
                move,
                initial_goto_duration=initial_goto,
            )
        except Exception as e:  # noqa: BLE001 - log and continue by design
            logger.error(f"async_play_move error for {move_name}: {e}")
            logger.error(traceback.format_exc())
            await asyncio.sleep(0.2)
            continue

        # micro pause to yield the loop
        await asyncio.sleep(0.02)


async def _sentiment_loop_async(
    stop_event: asyncio.Event,
    sentiment_state: SentimentState,
    *,
    question: str,
) -> None:
    """Poll sentiment periodically and update shared state (async)."""
    while not stop_event.is_set():
        label, score = await fetch_market_sentiment_async(AIKEK_API_URL, question=question)
        sentiment_state.label = label
        sentiment_state.score = score
        logger.info(f"[sentiment] label={label} score={score:.1f}")
        try:
            # wait with early exit on stop
            await asyncio.wait_for(stop_event.wait(), timeout=POLL_INTERVAL_SECONDS)
        except asyncio.TimeoutError:
            pass


async def async_main(*, question: str | None = None) -> None:
    """Run the Openfren application asynchronously.

    Args:
        question: Optional override for the question sent to the Alphakek API.
            If not provided, AIKEK_QUESTION environment variable is used, with a
            default fallback.
    """
    logger.info(
        f"Starting sentiment loop. API URL: {AIKEK_API_URL}; interval: {POLL_INTERVAL_SECONDS}s"
    )

    token = os.getenv("AIKEK_API_TOKEN")
    if not token:
        raise ValueError("AIKEK_API_TOKEN is not set")

    q = question or os.getenv("AIKEK_QUESTION", "crypto market sentiment now, one line")

    # Lazy imports to avoid heavy dependencies at import time for library users
    from reachy_mini import ReachyMini  # noqa: WPS433 - intentional local import
    from reachy_mini.motion.recorded_move import (  # noqa: WPS433 - intentional local import
        RecordedMoves,
    )

    recorded_moves = RecordedMoves(MOVES_DATASET)
    with ReachyMini(media_backend="default_no_video") as mini:
        mini.enable_motors()
        mini.media.play_sound("wake_up.wav")

        stop_event = asyncio.Event()
        sentiment_state = SentimentState(label=SentimentLabel.NEUTRAL, score=0.0)
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(
                    _movement_loop_async(mini, recorded_moves, stop_event, sentiment_state)
                )
                tg.create_task(
                    _sentiment_loop_async(stop_event, sentiment_state, question=q)
                )
                # Keep running until externally cancelled (Ctrl-C)
                await asyncio.Event().wait()
        except (asyncio.CancelledError, KeyboardInterrupt):
            logger.info("Interrupted by user. Shutting down...")
            stop_event.set()
        finally:
            mini.disable_motors()


def main(question: str | None = None) -> None:
    """Synchronous entrypoint for running Openfren locally."""
    try:
        asyncio.run(async_main(question=question))
    except KeyboardInterrupt:
        logger.info("Interrupted before connection. Exiting...")



