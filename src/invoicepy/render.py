from pathlib import Path
from typing import Optional

from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    StrictUndefined,
    select_autoescape,
)
from weasyprint import HTML

from invoicepy.const import DEFAULT_LOGO, DEFAULT_TEMPLATE_NAME
from invoicepy.models import Invoice


def _init_jinja_env(custom_templates_dir: Optional[Path]) -> Environment:
    loaders = []
    if custom_templates_dir is not None:
        loaders.append(FileSystemLoader(custom_templates_dir))
    loaders.append(PackageLoader("invoicepy"))
    loader = ChoiceLoader(loaders)
    return Environment(
        loader=loader,
        autoescape=select_autoescape(),
        undefined=StrictUndefined,
    )


def htmlstr_to_pdf(htmlstr: str, output_path: Path) -> Optional[bytes]:
    return HTML(string=htmlstr).write_pdf(output_path)


def render_invoice(
    invoice: Invoice, custom_templates_dir: Optional[Path], template_name: Optional[str]
) -> str:
    if template_name is None:
        template_name = "simple.html"
    template = _init_jinja_env(custom_templates_dir).get_template(template_name)
    return template.render(invoice=invoice, default_logo=DEFAULT_LOGO)


def write_pdf(
    invoice: Invoice,
    output_path: Path,
    custom_templates_dir: Optional[Path],
    template_name=Optional[str],
) -> Optional[bytes]:
    return htmlstr_to_pdf(
        render_invoice(
            invoice, custom_templates_dir, template_name or DEFAULT_TEMPLATE_NAME
        ),
        output_path,
    )
