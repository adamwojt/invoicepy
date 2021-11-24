#!/usr/bin/env python

"""Tests for `pyinvoice` package."""

from click.testing import CliRunner

from pyinvoice.cli.main import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    help_result = runner.invoke(cli, ["--help"])
    assert help_result.exit_code == 0
