Main operations of web app
==========================

Entry point
-----------
.. automodule:: webapp.app
    :members:

All web routes
--------------
.. automodule:: webapp.routes
    :members:

All socket channels
-------------------
.. automodule:: webapp.sockets
    :members:

Supporting modules
==================

Camera Manager
--------------
.. automodule:: webapp.inputs.camera_manager
    :members:

Virtual Terminal
----------------
.. automodule:: webapp.utils.virtual_terminal
    :members:

Fernet Vault
------------
.. automodule:: webapp.utils.file_encryption
    :members:

Super Logger
------------
.. automodule:: webapp.utils.super_logger
    :members:

User Management
===============
.. automodule:: webapp.users
    :members:
    :show-inheritance:

Configuration Management
========================
.. automodule:: webapp.config
    :members:

Constants
=========
.. autodata:: webapp.constants.TECH_USED
    :annotation:

.. autodata:: webapp.constants.PAGES_CONFIG
    :annotation:

.. autodata:: webapp.constants.SECRET_KEYFILE
    :annotation:

.. autodata:: webapp.constants.DB_CONFIG_FILE
    :annotation:

.. autodata:: webapp.constants.FLASK_SECRET_FILE
    :annotation:

.. autodata:: webapp.constants.ONE_YEAR
    :annotation:

.. autodata:: webapp.constants.DB_URI
    :annotation:

.. autodata:: webapp.constants.FLASK_SECRET
    :annotation:

.. autodata:: webapp.constants.LOCAL_DB_URI
    :annotation:

.. autodata:: webapp.constants.STATIC_CACHE_CONFIG
    :annotation:

Tools and scripts
=================

Generate Secret Key
-------------------

.. automodule:: tools.gen_secret_key
    :members:

Generate Flask secret
---------------------

.. automodule:: tools.gen_flask_secret
    :members:

Decrypt contents of encrypted files
-----------------------------------

.. automodule:: tools.decrypt_contents
    :members:

Initialize test database
------------------------

.. automodule:: tools.init_test_db
    :members:
