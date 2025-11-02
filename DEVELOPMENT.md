### Structure
- Library source: `src/openfren/`
- Public API (importables): `SentimentLabel`, `label_from_score`, `SentimentState`, `fetch_market_sentiment_async`
- CLI entrypoint: `openfren` → `openfren.cli:main`

### How it works
- `SentimentLabel`: bullish/neutral/bearish.
- `label_from_score(score: int) -> SentimentLabel`: clamps to [1, 10] and maps to a label.
- Async loops:
  - Movement loop: chooses moves and occasional sounds based on current label.
  - Sentiment loop: polls the Alphakek API and updates shared state.
  - App lifecycle uses `asyncio.TaskGroup` for clear startup/shutdown.

### Developer workflow (uv)
Install:
```bash
uv sync --dev
```

Format & lint (Ruff):
```bash
uv run ruff format
uv run ruff check
```

Type check (ty):
```bash
uvx ty check
```

Run tests:
```bash
uv run pytest -q
```

Build distributions:
```bash
uv build --no-sources
```

Version bump (examples):
```bash
uv version --bump patch
uv version --bump minor
uv version --bump major
```

Publish to PyPI (requires Trusted Publishing set up):
```bash
uv publish
```

### Pre-commit hooks
Install hooks (includes a pre-push pytest hook):
```bash
uv run pre-commit install
uv run pre-commit install --hook-type pre-push
```
Run on all files:
```bash
uv run pre-commit run --all-files
```
Update hooks (optional):
```bash
uv run pre-commit autoupdate
```

### Typing (ty) configuration
Project configuration lives in `pyproject.toml` under `[tool.ty]`. Source paths and excludes belong in `[tool.ty.src]`:
```toml
[tool.ty.src]
include = ["src", "tests"]
exclude = [".venv", "dist", "build", "wheels", "*.egg-info", "main.py"]
```
Reference: ty configuration docs: https://raw.githubusercontent.com/astral-sh/ty/refs/heads/main/docs/configuration.md

### Ruff tips
- Prefer `contextlib.suppress(asyncio.TimeoutError)` instead of bare `try`/`except`/`pass` to satisfy `SIM105`.
