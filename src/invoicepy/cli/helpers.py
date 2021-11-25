from pathlib import Path
from typing import List, Optional

import click

from invoicepy.models import Company, Customer, Invoice, InvoiceLine


def parse_invoice_lines(_, __, value: List[str] = None) -> List[InvoiceLine]:
    """Callback function for click parsing json invoice lines."""
    lines = []
    for line in value or []:
        try:
            lines.append(InvoiceLine.parse_raw(line))
        except Exception as e:
            raise click.BadParameter(
                f"Couldn't parse invoice line json:\n {line}."
            ) from e
    return lines


def parse_invoice(
    company: Company,
    customer: Customer,
    invoice_lines: List[InvoiceLine],
    invoice_due_date: Optional[str],
    invoice_number: Optional[int],
    invoice_currency: Optional[str],
    invoice_date: Optional[str],
    invoice_series: str,
) -> Invoice:
    """
    Parse parts to complete `Invoice` model.
    `None` args will be excluded so that default values can be loaded
    """
    _data = {
        "company": company,
        "customer": customer,
        "due_date": invoice_due_date,
        "series": invoice_series,
        "number": invoice_number,
        "lines": invoice_lines,
        "currency": invoice_currency,
        "create_date": invoice_date,
    }
    data = {k: v for k, v in _data.items() if v is not None}
    return Invoice(**data)


def determine_output_path(output_path: Optional[Path], invoice: Invoice) -> Path:
    """
    Return final output path to save the file, possible outcomes:
    1. output_path is `None` -> $CWD/$INVOICE_SLUG.pdf
    2. output_path is $DIR_PATH -> $DIR_PATH/$INVOICE_SLUG.pdf
    3. output_path is $FILE_PATH -> $FILE_PATH
    """
    if output_path is None or output_path.is_dir():
        filename = f"{invoice.slug}.pdf"
        output_path = (output_path or Path.cwd()) / filename
    return output_path
