from pyinvoice.models import Invoice


def test_invoice_calculated_fields(invoice_minimal):
    invoice = invoice_minimal
    assert invoice.currency == "EUR"
    assert invoice.get_currency_symbol() == "€"
    assert not invoice.has_vat_lines()
    assert invoice.name == "BAR0001"
    assert invoice.slug == "2011-11-11_bar-inc_bar0001"
    assert invoice.total_inc_tax == 8000
    assert invoice.total_tax == 0
    assert invoice.total_wo_tax == 8000


def test_invoice_with_vat(invoice_vat_usd):
    invoice = invoice_vat_usd
    assert invoice.get_currency_symbol() == "$"
    assert invoice.has_vat_lines()
    assert invoice.total_tax == 1760
    assert invoice.total_wo_tax == 8000
    assert invoice.total_inc_tax == 9760
