=========
pyinvoice
=========


.. image:: https://img.shields.io/pypi/v/invoice.svg
        :target: https://pypi.python.org/pypi/invoice


cli invoice tool, store and print invoices as pdf. save companies and customers for later use.

work in progress ...


installation
------------
.. code-block:: bash

    poetry install
    poetry shell

for now ...

config
------
.. code-block:: bash

    pyinvoice sample-config
    # then customize the gaps in $HOME/.pyinvoice.conf
    # config path can be specified with -C flag and PYINVOICE_CONFIG env var.

example usage
-------------

.. code-block:: bash

    # print pdf saving it in current directory, result is invoice nr. BAR001
    pyinvoice pdf --company foo --customer bar --line '{"price":10, "qty": 20, "name":"1h services"}' --series BAR

    # if above is repeated twice, the invoices numers will increase, BAR002, BAR003. This is calculated per series.
    # see below for more options.

CLI
---

.. code-block::

    pyinvoice [OPTIONS] COMMAND [ARGS]...

    Options:
      -C, --config PATH
      --help             Show this message and exit.

    Commands:

    sample-config: generate sample config in home dir

    pdf: prints pdf to given path

**pdf**


  -l, --line            json string of invoice line, can pass
                        multiple. ex: --line '{"price":15, "qty": 100,
                        "name":"1h cleaning services"}' --line ...
                        [required]

  -c, --company         company alias as in configuration.  [required]
  -r, --customer        customer alias as in configuration.
                        [required]

  -e, --due-date        if due date is not provided,
                        `payment_term_days` is used to calculate it.

  -s, --series          invoice series  [required]
  -n, --number          invoice number, if not provided, it will
                        calculated from company config for given
                        series.

  -u, --currency        currency, default=EUR
  -d, --date            invoice Date, `create_date` field.
  -o, --output          output path, can be new filepath, directory.
                        If it's not provided the invoice pdf will be
                        saved in current directory.

  -t, --template        template name, ex. simple.html.
                        `custom_templates_dir` will be searched first,
                        then package templates.
  --save                save invoice in config.
  --no-save             don't save in config.
  -b, --browser         Open generated invoice in browser.
  --help                Show this message and exit.


to-do
-----

- tests
- generate examples
- improve readme

nice-to-haves
-------------

- backup copy config on start
- invoices should have unique ids (maybe companies and customers too?)
- view saved invoices
- reprint saved invoices (?)
- tests

Credits
-------

This package was created with Cookiecutter_ and the `johanvergeer/cookiecutter-poetry`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`johanvergeer/cookiecutter-poetry`: https://github.com/johanvergeer/cookiecutter-poetry


Template taken from here and slightly modified:
https://github.com/sparksuite/simple-html-invoice-template

Licence
-------

Free software: MIT license
