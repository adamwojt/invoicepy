import webbrowser
from pathlib import Path
from typing import List, Optional

import click

from invoicepy.cli.helpers import determine_output_path, parse_invoice
from invoicepy.config import ConfigFile, write_sample_config
from invoicepy.models import InvoiceLine
from invoicepy.render import write_pdf


def command_sample_config(config_path: str):
    write_sample_config(config_path)


def command_pdf(
    configfile: ConfigFile,
    invoice_lines: List[InvoiceLine],
    company_alias: str,
    customer_alias: str,
    invoice_due_date: Optional[str],
    invoice_number: Optional[int],
    invoice_currency: Optional[str],
    invoice_date: Optional[str],
    invoice_series: str,
    output_path: Path,
    template_name: str,
    save: bool,
    open_in_browser: bool,
) -> Optional[Path]:
    company_config = configfile.config.get_company_config_by_alias(company_alias)
    if not company_config:
        raise ValueError(
            f"Company with alias `{company_alias}` is not configured, check your config."
        )
    customer_obj = configfile.config.get_customer_by_alias(customer_alias)
    if not customer_obj:
        raise ValueError(
            f"Customer with alias `{customer_alias}` is not configured, check your config."
        )
    if invoice_number is None:
        invoice_number = company_config.get_new_invoice_number_by_series(invoice_series)

    invoice = parse_invoice(
        company_config.company,
        customer_obj,
        invoice_lines,
        invoice_due_date,
        invoice_number,
        invoice_currency,
        invoice_date,
        invoice_series,
    )

    output_path = determine_output_path(output_path, invoice)
    # Make sure we don't override anything by prompting user.
    if output_path.exists() and not click.confirm(
        f"Are you sure you want to override existing file: {output_path} ?"
    ):
        click.echo("Aborting")
        return None

    # Render and write PDF.
    write_pdf(
        invoice,
        output_path,
        configfile.config.custom_templates_dir,
        template_name=template_name,
    )

    # Save invoice in user config if needed.
    if save:
        company_config.invoices.append(invoice)
        configfile.save()

    if open_in_browser:
        webbrowser.open(str(output_path))

    click.echo(f"Invoice pdf saved to {output_path}")
    return output_path
