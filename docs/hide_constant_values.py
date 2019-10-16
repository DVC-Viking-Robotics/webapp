"""
This is a monkey patch to hide constant values from the Flask docs. This is mainly since it can potentially expose
the values of sentitive constants such as the database URI and the Flask secret.

Source: https://stackoverflow.com/a/10870416
"""

# pylint: skip-file

def apply_monkey_patch():
    from sphinx.ext.autodoc import ModuleLevelDocumenter, DataDocumenter

    def add_directive_header(self, sig):
        ModuleLevelDocumenter.add_directive_header(self, sig)
        # Rest of original method ignored

    DataDocumenter.add_directive_header = add_directive_header
