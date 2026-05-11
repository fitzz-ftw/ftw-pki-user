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

class IncludeIfExists(Include):
    """Include a file only if it exists on disk."""

    def run(self) -> Sequence[Node]:
        # 1. Get the path from the directive argument
        raw_path = self.arguments[0]
        
        # 2. Get the directory of the current source file (cite: 1)
        current_source = Path(cast(str,self.state.document.current_source)).parent
        
        # 3. Resolve path: absolute or relative to the source file
        path = Path(raw_path)
        if not path.is_absolute():
            path = current_source / path
            
        # 4. Check existence without Sphinx util (cite: 1)
        if not path.exists():
            return []

        # 5. If it exists, let the standard Include directive handle it
        return super().run()

def setup(app):
    app.add_directive("include-if-exists", IncludeIfExists)
    return {'parallel_read_safe': True}
