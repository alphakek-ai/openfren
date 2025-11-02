import pytest


def test_cli_help_exits_zero():
    import openfren.cli as cli  # type: ignore[attr-defined]

    with pytest.raises(SystemExit) as e:
        cli.main(["--help"])  # argparse exits on --help
    assert e.value.code == 0


