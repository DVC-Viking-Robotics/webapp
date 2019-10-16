"""A config file for controlling the global behavior of the web app."""

DEBUG = False
"""A debug flag that controls flask's debug mode."""

LOCAL_DATABASE = False
"""
If set to true, it will attempt to use the local database via SQLITE.
You can initialize this database with ``python -m tools.init_test_db``
"""
