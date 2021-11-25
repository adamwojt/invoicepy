"""Main module."""

from datetime import date, timedelta
from typing import Dict, List, Optional

from pydantic import (
    BaseModel,
    ConstrainedStr,
    EmailStr,
    Field,
    FilePath,
    root_validator,
)

from invoicepy.const import CURRENCY_SYMBOLS_MAP
from invoicepy.utils import slugify


class InvoiceLine(BaseModel):
    name: str
    qty: float
    price: float
    vat: int = 0

    @property
    def total(self) -> float:
        return self.qty * self.price

    @property
    def vat_amount(self) -> float:
        return self.total * (self.vat / 100)


class Address(BaseModel):
    first_line: str
    second_line: Optional[str]
    post_code: str
    city: str
    country: str


class PaymentInformation(BaseModel):
    bank_name: str
    iban: str
    swift: str


class Company(BaseModel):
    name: str
    address: Address
    payment_information: PaymentInformation
    email: Optional[EmailStr]
    logo: Optional[FilePath]
    extra_info: Optional[str]

    class Config:
        validate_assignment = True


class Customer(BaseModel):
    name: str
    address: Address
    payment_term_days: int = 15
    email: Optional[EmailStr]


class Series(ConstrainedStr):
    min_length = 1
    max_length = 5
    strip_whitespace = True


class Currency(ConstrainedStr):
    min_length = 1
    max_length = 7
    strip_whitespace = True


class Invoice(BaseModel):
    series: Series
    number: int
    create_date: date = Field(default_factory=date.today)
    currency: Currency = Currency("EUR")
    company: Company
    customer: Customer
    due_date: Optional[date]
    lines: List[InvoiceLine]

    @root_validator(skip_on_failure=True)
    def calculate_due_date(cls, values: Dict) -> Dict:  # noqa
        if values["due_date"]:
            return values
        values["due_date"] = values["create_date"] + timedelta(
            days=values["customer"].payment_term_days
        )
        return values

    def has_vat_lines(self) -> bool:
        return any(line.vat > 0 for line in self.lines)

    def get_currency_symbol(self) -> Optional[str]:
        return CURRENCY_SYMBOLS_MAP.get(self.currency.upper())

    @property
    def slug(self) -> str:
        return slugify(
            f"{self.create_date.isoformat()}_{self.customer.name}_{self.name}"
        )

    @property
    def total_wo_tax(self) -> float:
        return sum(line.total for line in self.lines)

    @property
    def total_tax(self) -> float:
        return sum(line.vat_amount for line in self.lines)

    @property
    def total_inc_tax(self) -> float:
        return self.total_wo_tax + self.total_tax

    @property
    def name(self) -> str:
        return f"{self.series}{str(self.number).zfill(4)}"
