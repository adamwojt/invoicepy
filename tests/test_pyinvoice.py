#!/usr/bin/env python

"""Tests for `pyinvoice` package."""

import pytest

from click.testing import CliRunner

from pyinvoice import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
