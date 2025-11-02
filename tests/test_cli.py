import pytest


def test_cli_help_exits_zero():
    import openfren.cli as cli  # type: ignore[attr-defined]

    with pytest.raises(SystemExit) as excinfo:
        cli.main(["--help"])  # argparse exits on --help
    # SystemExit stores its exit code in args[0]
    assert (excinfo.value.args[0] if excinfo.value.args else None) == 0
