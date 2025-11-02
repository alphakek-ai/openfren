import argparse
from collections.abc import Sequence

from .app import main as app_main


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openfren",
        description=(
            "Your robot fren that reacts to Internet Capital Markets using Alphakek Fractal."
        ),
    )
    parser.add_argument(
        "--question",
        dest="question",
        type=str,
        help=(
            "Override AIKEK_QUESTION at runtime (env var still supported). "
            "Only this option is configurable."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    # Defer to the application entrypoint
    app_main(question=args.question)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


