.. _dev-building-docs:

How to build the docs locally
=============================

After preparing your Windows or Linux environment, install Spin and Ninja::

    pip install spin ninja

Then install the documentation-related dependencies::

    pip install -r util/readthedocs/requirements.txt

Then tell Spin to build the Sphinx documentation::

    spin docs

Then open a webserver to serve the built HTML files::

    python -m http.server -d doc/build/html 8000

And open your local docs in a web browser by visiting http://localhost:8000/.

If it's your first time building the docs, it will take a while but should go
faster on subsequent re-builds.
