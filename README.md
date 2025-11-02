## Openfren

Proof-of-Concept. Your robot fren that reacts to changes in Internet Capital Markets using Alphakek Fractal knowledge engine as its 
brain. Free and open source.

[![CI](https://img.shields.io/github/actions/workflow/status/alphakek-ai/openfren/ci.yml?branch=master)](https://github.com/alphakek-ai/openfren/actions)
[![PyPI](https://img.shields.io/pypi/v/openfren.svg)](https://pypi.org/project/openfren/)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE.md)
![Python](https://img.shields.io/badge/python-3.13%20%7C%203.14-blue)

[Release notes](CHANGELOG.md)

### TODO

- [ ] Fractal 2 integration
- [ ] Voice commands
  - [ ] Conversation mode
- [ ] Face tracking
  - [ ] Emotion recognition
  - [ ] Face recognition (local, on-device)

### Installation
Using `uv` (recommended for dev):
```bash
uv sync
```

From PyPI (runtime only):
```bash
pip install openfren
```

### Configuration
- Environment variables (only these are configurable):
  - `AIKEK_API_TOKEN` — required. Obtain one at https://app.alphakek.ai
  - `AIKEK_QUESTION` — optional, default: "crypto market sentiment now, one line"

You may pass environment variables directly or via a `.env` file. See `env.example` for a template.

### Run
If you don't have the physical robot yet, first start the simulation:
```bash
uv run reachy-mini-daemon --sim --scene minimal
```
If you have a robot, just start the daemon:
```bash
uv run reachy-mini-daemon
```
Then start Openfren:
```bash
uv run openfren
```

### Test
```bash
uv run pytest
```

### Notes
- Developed and regularly tested on Linux. macOS/Windows should work (best‑effort), but are not as thoroughly validated.
- Requires Reachy Mini hardware or the simulator daemon.

### Development
See [DEVELOPMENT.md](DEVELOPMENT.md) for architecture overview and contributor/developer details.

### Credits
- Reachy Mini by Pollen Robotics
- Emotions dataset: `pollen-robotics/reachy-mini-emotions-library`


