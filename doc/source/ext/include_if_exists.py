"""
Include-if-exists Sphinx extension. (rw)

To use this extension, add its module name to the extensions list in conf.py:
    extensions = [
        ...
        'include_if_exists',
    ]
"""
from pathlib import Path
from typing import Sequence, cast
from docutils.nodes import Node
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.misc import Include
from sphinx.util.osutil import adapt_path

class IncludeIfExists(Include):
    """Include a file only if it exists on disk."""
    def run(self) -> Sequence[Node]:
        path = directives.path(self.arguments[0])
        if path.startswith('<') and path.endswith('>'):
            path = '/' + path[1:-1]
            root_prefix = self.standard_include_path
        else:
            root_prefix = self.state.document.settings.root_prefix
        
        path = adapt_path(path, cast(str, self.state.document.current_source), root_prefix)
        
        if not Path(path).exists():
            return []

        return super().run()

def setup(app):
    app.add_directive("include-if-exists", IncludeIfExists)
    return {'parallel_read_safe': True}
