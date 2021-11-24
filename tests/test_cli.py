#!/usr/bin/env python

"""Tests for `pyinvoice` package."""

import click
import pytest
from click.testing import CliRunner

from pyinvoice.cli.helpers import parse_invoice_lines
from pyinvoice.cli.main import cli


def test_pdf_command(correct_pdf_args, output_path_temp):
    """Integration test full pdf command"""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    help_result = runner.invoke(cli, ["--help"])
    assert help_result.exit_code == 0
    result = runner.invoke(cli, correct_pdf_args)
    assert output_path_temp.exists()


def test_parse_invoice_lines_callback(invoice_line):
    json_line = invoice_line.json()
    res = parse_invoice_lines(None, None, [json_line])
    assert invoice_line == res[0]


def test_parse_invoice_lines_callback_fail(invoice_line):
    json_line = invoice_line.json()
    with pytest.raises(click.BadParameter):
        parse_invoice_lines(None, None, [json_line[:5]])
