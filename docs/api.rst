Main operations of web app
==========================

Entry point
-----------
.. automodule:: webapp.app
    :members:
    :inherited-members:

All web routes
--------------
.. automodule:: webapp.routes
    :members:
    :inherited-members:

All socket channels
-------------------
.. automodule:: webapp.sockets
    :members:
    :inherited-members:

Supporting modules
==================

Camera Manager
--------------
.. automodule:: webapp.inputs.camera_manager
    :members:
    :inherited-members:

Virtual Terminal
----------------
.. automodule:: webapp.utils.virtual_terminal
    :members:
    :inherited-members:

Fernet Vault
------------
.. automodule:: webapp.utils.file_encryption
    :members:
    :inherited-members:

User Management
===============
.. automodule:: webapp.users
    :members:
    :show-inheritance:

Configuration Management
========================
.. automodule:: webapp.config
    :members:
    :inherited-members:

Constants
=========
.. autodata:: webapp.constants.TECH_USED
    :annotation: = A exhaustive list of all the technology used for this project.

.. autodata:: webapp.constants.PAGES_CONFIG
    :annotation: = A front-end configuration for the arrangement of the page tiles for the home page.

.. autodata:: webapp.constants.SECRET_KEYFILE
    :annotation: = Location of master secret keyfile for DB URI and Flask secret encryption.

.. autodata:: webapp.constants.DB_CONFIG_FILE
    :annotation: = Location of encrypted DB URI file.

.. autodata:: webapp.constants.FLASK_SECRET_FILE
    :annotation: = Location of encrypted flask secret file.

.. autodata:: webapp.constants.ONE_YEAR
    :annotation: = The time of one year in seconds.

.. autodata:: webapp.constants.DB_URI
    :annotation: = The database URI for facilitating user management.

.. autodata:: webapp.constants.FLASK_SECRET
    :annotation: = Used by Flask to securely sign cookies.
.. autodata:: webapp.constants.LOCAL_DB_URI
    :annotation: = Database URI used when using local database. See `config.LOCAL_DATABASE` for more info.
.. autodata:: webapp.constants.STATIC_CACHE_CONFIG
    :annotation: = Configuration for cache busting common static files.