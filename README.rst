====
LOOG
====

An Odoo log parsing and enrichment library and CLI.

Installation
============

For use as a command line tool `pipx <https://pypi.org/project/pipx/>`_
is a good way to install it::

    pipx install "loog @ git+https://github.com/laurent-corron/loog"

The usual installation mechanism with pip also works of course::

   python -m pip install --user "loog @ git+https://github.com/laurent-corron/loog"

Quick start
===========

After installing, running ``loog < odoo.log`` will parse the log and output
enriched JSON records for each log entry.

Log records have the following basic fields:

- asctime
- pid
- levelname: DEBUG, INFO, WARNING, ERROR, CRITICAL
- dbname
- logger
- message

Enrichment features
-------------------

Detect ``werkzeug`` records for HTTP requests and add the following fields:

- remote_addr
- request_method: GET, POST, ...
- status: 200, 500, ...
- request_uri
- request_path
- sql_count (int)
- sql_time (float)
- other_time (float)
- total_time (float)

Using loog as a library
=======================

``loog`` has a public API so it's feature are readily available for you to
develop custom Odoo log processing pipelines.

TODO - document the API.

Development
===========

To work with this project create a virtual environment, and install the project
in development mode

.. code-block:: console

   $ python3 -m venv env
   $ env/bin/pip install -e .

This project uses black, isort, flake8 and other tools for code formating and linting.
To ensure your contributions follow the conventions, install `pre-commit
<https://pre-commit.com/>`_, then run ``pre-commit install`` in the directory where you
cloned the project.

Running the tests
-----------------

This project uses pytest for testing.

To run all tests with your default python 3, use::

   tox -e py3

Authors
=======

* `Laurent Corron <https://github.com/Laurent-Corron>`_
* `Stéphane Bidoul <https://github.com/sbidoul>`_

See also the list of `contributors
<https://github.com/Laurent-Corron/loog/contributors>`_ who participated in this
project.

License
=======

This project is under the MIT license - see the LICENSE file for details.
