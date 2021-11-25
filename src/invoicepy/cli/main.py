"""Console script for invoicepy."""
import sys
from pathlib import Path

import click

from invoicepy.cli.commands import command_pdf, command_sample_config
from invoicepy.cli.helpers import parse_invoice_lines
from invoicepy.config import ConfigFile


@click.group()
@click.option("--config", "-C", envvar="PYINVOICE_CONFIG", type=click.Path())
@click.pass_context
def cli(ctx, config):
    if ctx.invoked_subcommand == "sample-config":
        command_sample_config(config)
        return
    ctx.obj = ConfigFile(config)


@cli.command()
def sample_config():
    """Done in cli group command"""
    pass


@cli.command()
@click.option(
    "--line",
    "-l",
    multiple=True,
    required=True,
    type=str,
    callback=parse_invoice_lines,
    help="""json string of invoice line, can pass multiple.
ex: --line \'{"price":15, "qty": 100, "name":"1h cleaning services"}\' --line ...""",
)
@click.option(
    "--company",
    "-c",
    required=True,
    type=str,
    help="Company alias as in configuration.",
)
@click.option(
    "--customer",
    "-r",
    required=True,
    type=str,
    help="Customer alias as in configuration.",
)
@click.option(
    "--due-date",
    "-e",
    type=str,
    help="If due date is not provided, `payment_term_days` is used to calculate it.",
)
@click.option("--series", "-s", required=True, type=str, help="Invoice series")
@click.option(
    "--number",
    "-n",
    type=int,
    help="Invoice number, if not provided, it will calculated from company config for given series.",
)
@click.option("--currency", "-u", type=str, help="Currency, default=EUR")
@click.option("--date", "-d", type=str, help="Invoice Date, `create_date` field.")
@click.option(
    "--output",
    "-o",
    type=click.Path(exists=False, path_type=Path),
    help="""Output path, can be new filepath, directory. If it's not provided
the invoice pdf will be saved in current directory.""",
)
@click.option(
    "--template",
    "-t",
    type=str,
    help="Template name, ex. simple.html. `custom_templates_dir` will be searched first, then package templates.",
)
@click.option(
    "--save/--no-save",
    default=True,
    help="Decides whether to store invoice in config file.",
)
@click.option(
    "--browser",
    "-b",
    is_flag=True,
    default=False,
    help="Open generated invoice in browser.",
)
@click.pass_obj
def pdf(
    configfile,
    line,
    company,
    customer,
    due_date,
    number,
    currency,
    date,
    output,
    series,
    template,
    save,
    browser,
):
    command_pdf(
        configfile=configfile,
        invoice_lines=line,
        company_alias=company,
        customer_alias=customer,
        invoice_due_date=due_date,
        invoice_number=number,
        invoice_currency=currency,
        invoice_date=date,
        invoice_series=series,
        template_name=template,
        output_path=output,
        save=save,
        open_in_browser=browser,
    )


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
