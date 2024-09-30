books-api
=========

.. image:: https://github.com/amikrop/books-api/actions/workflows/main.yml/badge.svg
   :target: https://github.com/amikrop/books-api/actions/
   :alt: Workflows

This is a demo backend providing some basic book management, made using Django REST Framework.

It is tested for Python versions 3.8 - 3.12.

Usage
-----

Build and run the Docker containers:

.. code-block:: bash

   $ docker-compose up --build

Schema
------

API schema documentation can be accessed at:

- `http://localhost:8000/schema/`
- `http://localhost:8000/schema/swagger-ui/`
- `http://localhost:8000/schema/redoc/`

Unit tests
----------

Multiple Python versions
************************

Run the tests for all supported Python versions found in your system, using `tox <https://tox.wiki/>`_:

.. code-block:: bash

   $ cd app
   $ tox

In-container
************

Once you have started the Docker app, you can run the tests for the containerized deployment:

.. code-block:: bash

   $ docker-compose run web pytest
