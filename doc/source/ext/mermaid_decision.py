"""
Utility functions and factory methods for documentation builds. (rw)

This module contains logic that is not a direct Sphinx extension but 
provides helper functionality for configuration and build decisions.

To use these utilities, import them in your conf.py:
    from utils import create_mermaid_decision_maker
    inherit_diagramm: list[str] = []
    exclude_inherit_diagramm: list[str] = []
    autosummary_context = {
        ...
        "inheritence_diagram": create_mermaid_decision_maker(
                    inherit_diagramm, exclude_inherit_diagramm
                ),
        ...
        }

"""


from collections.abc import Callable
import importlib


def create_mermaid_decision_maker(whitelist:list[str]|None=None, 
                                  blacklist:list[str]|None=None) -> Callable[..., bool]:
    """
    Factory that creates a decision function for Mermaid diagram rendering.

    The returned function evaluates whether a class or module should have 
    a Mermaid diagram generated based on a cost-optimized hierarchy:
    1. Blacklist check (lowest cost)
    2. Whitelist check
    3. Dynamic import and base class analysis (highest cost)

    :param whitelist: List of full paths to include.
    :param blacklist: List of full paths to exclude.
    :return: A callable that returns True if Mermaid should be rendered.
    """
    whitelist = whitelist or []
    blacklist = blacklist or []

    def should_render_mermaid(fullname) -> bool:
        """
        Determine if a specific object should render a Mermaid diagram. (rw)
        
        :param fullname: The full python path of the object (e.g., 'module.Class').
        :return: True if rendering is allowed, False otherwise.
        """
        # 1. FAST RETURN: Blacklist
        # If explicitly forbidden, exit immediately.   
        if fullname in blacklist:
            return False

        # 2. FAST RETURN: Whitelist
        # If explicitly allowed, exit immediately.
        if fullname in whitelist:
            return True

        # 3. HEAVY LIFTING: Import & Analysis
        # Only start the import machine if lists provide no answer.
        try:
            if "." not in fullname:
                return False

            module_name, class_name = fullname.rsplit(".", 1)
            module = importlib.import_module(module_name)
            obj = getattr(module, class_name)

            if isinstance(obj, type):
                return any(b.__name__ != "object" for b in obj.__bases__)

            return False
        except (ImportError, AttributeError, ValueError):
            return False

    return should_render_mermaid
