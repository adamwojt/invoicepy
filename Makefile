# Some dev script(s)

.PHONY: update-schema

define SCHEMA_UPDATE
import json
from invoicepy.models import Invoice
from invoicepy.config import Config
with open('src/invoicepy/schema/invoice.json', 'w') as fh:
	fh.write(Invoice.schema_json(indent=4))

with open('src/invoicepy/schema/config.json', 'w') as fh:
	fh.write(Config.schema_json(indent=4))
endef
export SCHEMA_UPDATE

update-schema:
	poetry run python -c "$$SCHEMA_UPDATE"
