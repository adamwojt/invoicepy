# Some dev script(s)

.PHONY: update-schema

define SCHEMA_UPDATE
import json
from pyinvoice.models import Invoice
from pyinvoice.config import Config
with open('src/pyinvoice/schema/invoice.json', 'w') as fh:
	fh.write(Invoice.schema_json(indent=4))

with open('src/pyinvoice/schema/config.json', 'w') as fh:
	fh.write(Config.schema_json(indent=4))
endef
export SCHEMA_UPDATE

update-schema:
	poetry run python -c "$$SCHEMA_UPDATE"
