# LOOG

An Odoo log parsing and enrichment library and CLI.

## Quick start

After installing, running `loog < odoo.log` will parse the log and output
enriched JSON records for each log entry.

Enrichment features include:

- detect `werkzeug` records for HTTP requests and add HTTP status, URI,
  performance information

`loog` has a public API so it's feature are readily available for you to
develop custom Odoo log processing pipelines.

## Development

To work with this project create a virtual environment, and install the project
in development mode.

```console
$ python3 -m venv env
$ env/bin/pip install -e .
```

This project uses black, isort, flake8 and other tools for code formating and
linting. To ensure your contributions follow the conventions, install
[pre-commit](<https://pre-commit.com/>), then run `pre-commit install` in the
directory where you cloned the project.

## Running the tests

This project uses pytest for testing.

To run all tests with your default python 3, use:

```
tox -e py3
```

## Authors

* [Laurent Corron](https://github.com/Laurent-Corron)
* [Stéphane Bidoul](https://github.com/sbidoul)

See also the list of
[contributors](https://github.com/Laurent-Corron/loog/contributors) who
participated in this project.

## License

This project is under the MIT license - see the [LICENSE](LICENSE) file for details
