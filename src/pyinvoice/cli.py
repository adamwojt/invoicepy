"""Console script for pyinvoice."""
import sys
import webbrowser

from pathlib import Path
from typing import List

import click

from pyinvoice.config import ConfigFile, write_sample_config
from pyinvoice.models import Invoice, InvoiceLine
from pyinvoice.render import write_pdf
from pyinvoice.utils import slugify


@click.group()
@click.option("--config", "-C", envvar="INVOICE_CONFIG", type=click.Path())
@click.pass_context
def main(ctx, config):
    if ctx.invoked_subcommand == "sample-config":
        write_sample_config(config)
    else:
        ctx.obj = ConfigFile(config)


def parse_invoice_lines(ctx, param, value: List[str] = None) -> List[InvoiceLine]:
    lines = []
    for line in value or []:
        try:
            lines.append(InvoiceLine.parse_raw(line))
        except Exception as e:
            raise click.BadParameter(
                f"Couldn't parse invoice line json:\n {line}."
            ) from e
    return lines


@main.command()
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
    "-dd",
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
@click.option("--date", "-da", type=str, help="Invoice Date, `create_date` field.")
@click.option(
    "--output",
    "-o",
    type=click.Path(exists=False),
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
    # Init config
    company_config = configfile.config.get_company_config_by_alias(company)
    if not company_config:
        raise ValueError(
            f"Company with alias `{company}` is not configured, check your config."
        )
    customer_obj = configfile.config.get_customer_by_alias(customer)
    if not customer_obj:
        raise ValueError(
            f"Customer with alias `{customer}` is not configured, check your config."
        )
    if number is None:
        number = company_config.get_new_invoice_number_by_series(series)

    # Parse data
    _data = {
        "company": company_config.company,
        "customer": customer_obj,
        "due_date": due_date,
        "series": series,
        "number": number,
        "lines": line,
        "currency": currency,
        "create_date": date,
    }
    data = {k: v for k, v in _data.items() if v is not None}
    invoice = Invoice(**data)

    # If no output or output is directory, create filename, otherwise use path as is.
    if (output is None) or Path(output).is_dir():
        base_name = slugify(
            f"{invoice.create_date.isoformat()}_{invoice.customer.name}_{invoice.series}{invoice.number}"
        )
        filename = f"{base_name}.pdf"
        output_path = (Path(output) if output else Path.cwd()) / filename
    else:
        output_path = Path(output)

    # Make sure we don't override anything by prompting user.
    if output_path.exists() and not click.confirm(
        f"Are you sure you want to override existing file: {output_path} ?"
    ):
        click.echo("Aborting")
        return

    # Render and write PDF.
    write_pdf(
        invoice,
        output_path,
        configfile.config.custom_templates_dir,
        template_name=template or "simple.html",
    )

    # Save invoice in user config if needed.
    if save:
        company_config.invoices.append(invoice)
        configfile.save()

    if browser:
        webbrowser.open(str(output_path))


@main.command()
def sample_config():
    pass


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
