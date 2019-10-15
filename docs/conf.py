# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# pylint: skip-file

import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'MASCCOT web app'
copyright = '2019, Tejas Shah'
author = 'Tejas Shah'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u'1.0'
# The full version, including alpha/beta/rc tags.
release = u'1.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'recommonmark',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode'
]

# TODO: Please Read!
# Uncomment the below if you use native CircuitPython modules such as
# digitalio, micropython and others. List the modules you use. Without it, the
# autodoc module docs will fail to generate with a warning.
# autodoc_mock_imports = ["digitalio", "pulseio", "serial", "circuitpython_nrf24l01"]

# the default order of documented memebers using autodoc extension.
# Default is alphabetical :(
autodoc_member_order = 'bysource'

# Used for referencing objects from other libraries/packages.
# The first item is needed to link the user to builtin datatypes
# (like `list` or `tuple`) using python docs
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.6', None)
    }

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.env']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    try:
        import sphinx_rtd_theme
        html_theme = 'sphinx_rtd_theme'
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path(), '.']
    except:
        html_theme = 'default'
        html_theme_path = ['.']
else:
    html_theme_path = ['.']

html_logo = '../webapp/static/images/viking.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'darkness.css',
]

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#
html_favicon = '_static/favicon.ico'

# The reST default role (used for this markup: `text`) to use for all
# documents.
#
default_role = "any"

# If true, '()' will be appended to :func: etc. cross-reference text.
#
add_function_parentheses = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# If this is True, todo emits a warning for each TODO entries. The default is False.
todo_emit_warnings = False

napoleon_numpy_docstring = False
