"""
Custom roles for text styling and cross-referencing. (rw)

To use these roles, add the following to your conf.py setup(app) function:
    app.add_role('ftwpatchopt', ftwpatchopt_role)
    app.add_role('ftwoption', ftwoption_role)
    app.add_role('person', person_role)
"""
from docutils import nodes

def ftwpatchopt_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """Custom role for monospace text styling using the 'ftwpatchopt' class."""
    node = nodes.literal(rawtext, text, classes=['ftwpatchopt'])
    return [node], []

def ftwoption_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """
    Custom Sphinx role to link to CLI options.
    Creates a literal node wrapped in a reference to an 'opt-<text>' ID.
    """
    inner_node = nodes.literal(rawtext, text, classes=["ftw-opt-link", "custom-option-style"])
    target_id = nodes.make_id(f"opt-{text}")
    ref_node = nodes.reference(rawtext, "", internal=True, refid=target_id)
    ref_node += inner_node
    return [ref_node], []

def person_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """Custom role for person names, styled via the 'person' CSS class (e.g., small-caps)."""
    node = nodes.inline(rawtext, text, classes=["person"])
    return [node], []
