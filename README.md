
pyinvoice
=========
<img src="examples/2021-11-23_bar-inc_bar1.png" alt="invoice" width="400"/>

**CLI** invoice tool, store and print invoices as *pdf*. save companies and
customers for later use.


installation
------------

``` {.sourceCode .bash}
poetry install
poetry shell
```

for now ...

config
------

``` {.sourceCode .bash}
pyinvoice sample-config
# then customize it in $HOME/.pyinvoice.conf
# config path can be specified with -C flag and PYINVOICE_CONFIG env var.
```

example
-------------

Print pdf saving it in current directory, result is invoice nr. BAR001
``` {.sourceCode .bash}
pyinvoice pdf --company foo --customer bar --line '{"price":10, "qty": 20, "name":"1h services"}' --series BAR
```
when above is repeated twice, the invoices numers will increase, BAR002, BAR003. this is calculated per series.
see below for more options.

cli
---

``` {.sourceCode .}
pyinvoice [OPTIONS] COMMAND [ARGS]...

Options:
  -C, --config PATH
  --help             Show this message and exit.

Commands:

sample-config: generate sample config in home dir

pdf: prints pdf to given path
```

**pdf**

```
Options:
  -l, --line TEXT       json string of invoice line, can pass multiple. ex:
                        --line '{"price":15, "qty": 100, "name":"1h cleaning
                        services"}' --line ...  [required]

  -c, --company TEXT    company alias as in configuration.  [required]
  -r, --customer TEXT   customer alias as in configuration.  [required]
  -e, --due-date TEXT   If due date is not provided, `payment_term_days` is
                        used to calculate it.

  -s, --series TEXT     invoice series  [required]
  -n, --number INTEGER  invoice number, if not provided, it will calculated
                        from company config for given series.

  -u, --currency TEXT   currency, default=EUR
  -d, --date TEXT       invoice Date, `create_date` field.
  -o, --output PATH     output path, can be new filepath, directory. If it's
                        not provided the invoice pdf will be saved in current
                        directory.

  -t, --template TEXT   template name, ex. simple.html. `custom_templates_dir`
                        will be searched first, then package templates.

  --save / --no-save    decides whether to store invoice in config file.
  -b, --browser         open generated invoice in browser.
  --help                show this message and exit.
```

to-do
-----

-   tests
-   upload to pip

nice-to-haves
-------------

-   consider moving config to yaml
-   backup copy config on start
-   invoices should have unique ids (maybe companies and customers too?)
-   view saved invoices
-   reprint saved invoices (?)
-   package for arch (AUR)

Credits
-------

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[johanvergeer/cookiecutter-poetry](https://github.com/johanvergeer/cookiecutter-poetry)
project template.

Template taken from here and slightly modified:
<https://github.com/sparksuite/simple-html-invoice-template>

Licence
-------

Free software: MIT license
