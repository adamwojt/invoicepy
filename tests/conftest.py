import shutil
from pathlib import Path

import pytest
from _pytest import config

from invoicepy.config import ConfigFile
from invoicepy.models import Invoice, InvoiceLine


@pytest.fixture
def root_project_dir():
    return Path(__file__).parent.parent


@pytest.fixture
def sample_config_path(root_project_dir):
    return root_project_dir / "src" / "invoicepy" / "config" / "sample_config.json"


@pytest.fixture
def sample_config_file(sample_config_path):
    return ConfigFile(sample_config_path)


@pytest.fixture
def company(sample_config_file):
    return sample_config_file.config.companies[0].company


@pytest.fixture
def customer(sample_config_file):
    return sample_config_file.config.customers[0].customer


@pytest.fixture
def invoice_minimal(company, customer, series, invoice_line):
    return Invoice(
        **{
            "company": company,
            "customer": customer,
            "series": series,
            "lines": [invoice_line],
            "number": 1,
            "create_date": "2011-11-11",
        }
    )


@pytest.fixture
def invoice_vat_usd(company, customer, series, vat_invoice_line):
    return Invoice(
        **{
            "company": company,
            "customer": customer,
            "series": series,
            "lines": [vat_invoice_line],
            "number": 1,
            "create_date": "2011-11-11",
            "due_date": "2011-11-12",
            "currency": "USD",
        }
    )


@pytest.fixture
def sample_config_temp(sample_config_path, tmp_path):
    config_path = tmp_path / ".invoicepy.conf"
    shutil.copy(sample_config_path, config_path)
    return config_path


@pytest.fixture
def output_path_temp(tmp_path):
    return tmp_path / "test_invoice.pdf"


@pytest.fixture
def company_alias():
    return "foo"


@pytest.fixture
def customer_alias():
    return "bar"


@pytest.fixture
def series():
    return "BAR"


@pytest.fixture
def correct_pdf_args(
    sample_config_temp, customer_alias, company_alias, invoice_line, output_path_temp
):
    return [
        "-C",
        str(sample_config_temp),
        "pdf",
        "--customer",
        customer_alias,
        "--company",
        company_alias,
        "--line",
        invoice_line.json(),
        "--series",
        "BAR",
        "--output",
        output_path_temp,
    ]


@pytest.fixture
def invoice_line():
    return InvoiceLine(**{"price": 50, "name": "1h programming", "qty": 160})


@pytest.fixture
def vat_invoice_line():
    return InvoiceLine(**{"price": 50, "name": "1h programming", "qty": 160, "vat": 22})
