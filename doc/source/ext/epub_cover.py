"""
Utility for generating documentation cover pages. (rw)

This module handles the rendering of SVG covers using Jinja2 templates,
specifically for EPUB and HTML builds.

To use this utility, import it in your conf.py:
    from epub_cover import render_cover
"""
import os

from jinja2 import Environment, FileSystemLoader


def render_cover(
    programname: str, version: str, covertemplate: str = "cover.svg"
) -> tuple[str, str]:
    """
    Renders an SVG cover page with project metadata. (rw)

    The function looks for a template in '_templates', processes it with 
    Jinja2, and saves the output to '_static'.

    :param programname: Name of the project/program to display.
    :param version: Version or release string to display.
    :param covertemplate: The filename of the SVG template in '_templates'.
    :return: A tuple of (output_path, epub_hint_string).
    """
    templates_dir = "_templates"
    static_dir = "_static"

    # Ensure the static directory exists for the output
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template(covertemplate)

    # Render the template with the provided project variables
    output_path = os.path.join(static_dir, covertemplate)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template.render(version=version, programname=programname))
    return (output_path, "epub-cover.html")
