# Configuration file for the Sphinx documentation builder.
from collections.abc import Callable
import os
import sys
from pathlib import Path
CONF_DIR = Path(__file__).parent
sys.path.insert(0, str((CONF_DIR / "ext").absolute()))

# Read the Docs liefert uns die Canonical URL direkt!
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

# Falls wir lokal sind, ist die Variable leer, dann setzen wir einen Fallback
if not html_baseurl:
    html_baseurl = "/"


try:
    from ftwpki.user._version import __version__ # type: ignore
    version = __version__ # pyright: ignore[reportUndefinedVariable]
    release = __version__ # pyright: ignore[reportUndefinedVariable]
except ImportError:
    version = '1.0'  # Fallback, damit ePub nicht meckert
    release = '1.0.0'

#SECTION - Custom Includes
#SECTION - Import Custom Includes
from roles import  ftwpatchopt_role, ftwoption_role, person_role # pyright: ignore[reportMissingImports]
from transforms import inject_option_anchors, InjectArgparseAnchors # pyright: ignore[reportMissingImports]
#!SECTION - Import Custom Includes
#SECTION - Register Custom Includes
def setup(app):
    """Register custom components during the Sphinx setup process."""
    app.add_role('ftwpatchopt', ftwpatchopt_role)
    app.add_role("ftwoption", ftwoption_role)
    app.add_role("person", person_role)
    app.connect("doctree-read", inject_option_anchors)
    app.add_transform(InjectArgparseAnchors)
    InjectArgparseAnchors.default_priority = 10
#!SECTION - Register Custom Includes
#!SECTION - Custom Includes


#SECTION - Project information -----------------------------------------------------
project = "ftw-user"
copyright = "2026, Fitzz TeΧnik Welt"
author = "Fitzz TeΧnik Welt"
html_show_copyright = True
language = "en"
#!SECTION - Project information -----------------------------------------------------

#SECTION - General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",  # Zuerst die Basis
    "sphinx.ext.intersphinx",  # Wichtig für Cross-Refs
    "sphinx.ext.autosummary",
    "myst_parser",  # Falls du Markdown nutzt
    "sphinxarg.ext",  # Das "tote Pferd" erst jetzt laden
    "autoclasstoc",
    "sphinxarg.ext",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
    "include_if_exists",
]


templates_path = ["_templates", "_templates/autosummary"]
exclude_patterns = []
maximum_signature_line_length= 120
toc_object_entries_show_parents='hide'
suppress_warnings=[
    'autosummary.import_cycle',
    'config.cache',
]

#!SECTION - General configuration ---------------------------------------------------



#SECTION - Options for HTML output -------------------------------------------------
html_theme = "sphinx_nefertiti"
html_theme_options = {
    "style": "indigo",
    "documentation_font_size": "1.2rem",
    "header_links": [
        {
            "text": "Index",
            "link": "genindex",
        },
        {
            "text": "List of Modules",
            "link": "py-modindex",
        },
    ],
    "logo": "ftw-initials.svg",
    "logo_height": 40,
    "logo_width": 40*1.2,
    "logo_location": "header",
    # "header_links_in_2nd_row": True,
    "project_name_font": "Fira Sans",
    "doc_headers_font": "Fira Sans",
    "documentation_font": "Fira Sans",
    "sans_serif_font": "Fira Sans",
    "monospace_font": "Fira Code",
}

html_static_path = ["_static"]
html_css_files = ["custom_nefertiti_html.css"]
toc_object_entries = True
toc_object_entries_show_parents = "hide"

#!SECTION - Options for HTML output -------------------------------------------------



#SECTION - Options for Intersphinx
intersphinx_mapping = {
    "python": (f"https://docs.python.org/{sys.version_info.major}.{sys.version_info.minor}", None),
    "platformdirs": ("https://platformdirs.readthedocs.io/en/latest/", None),
}
#!SECTION - Options for Intersphinx

#SECTION - Options for ePub output -------------------------------------------------
from epub_cover import render_cover # pyright: ignore[reportMissingImports]
if "epub" in sys.argv:
    epub_cover = render_cover("ftw-user", version.split("+")[0])


epub_theme = 'epub'
epub_basename = 'FTW_Development_Tools_Manual'
epub_title = project
epub_author = author
epub_publisher = author
# epub_identifier = 'https://github.com/ftwpki.user.git'
epub_scheme = 'URL'
epub_css_files = ['custom_epub.css']
# Fügt den Index und Modulindex zum internen Guide hinzu
epub_use_index = True  # Erlaubt die Generierung des Index
# Dies erzwingt die Aufnahme in das Inhaltsverzeichnis des Readers
epub_tocscope = 'default'
epub_tocdepth = 3

auto_exclude_files=[]
if "epub" in sys.argv:
    woff2_files = [str(file_) for file_ in Path().rglob("*.woff2")]
    fira_fonts= [str(file_) for file_ in Path().rglob("fira-*/*")]
    auto_exclude_files=list(set([*woff2_files,*fira_fonts]))


epub_exclude_files = [
    "_static/fonts/GUST-FONT-LICENSE.txt",
    "_static/fonts/OFL.md",
    "_static/fonts/OFL.txt",
    ".buildinfo.bak",
    *auto_exclude_files,
]

#!SECTION - Options for ePub output -------------------------------------------------

#SECTION - Options for Mermaid -----------------------------------------------------
mermaid_use_local = "_static/mermaid.min.js"
#!SECTION - Options for Mermaid -----------------------------------------------------


#SECTION - Autodoc / Autosummary configuration -------------------------------------
#SECTION - Options for Autodoc
autodoc_typehints = "description"
autodoc_class_signature = "separated"
autodoc_typehints_description_target = "documented_params"
autodoc_default_options = {
    "members": True,
    'special-members': False,
    # 'private-members': "_ANSI,_color_map",
    #    'inherited-members': False,
    # 'undoc-members': True,
    "exclude-members": "__weakref__,__new__",
    "class-doc-from": "class",
}

if sys.version_info < (3, 14):
    autodoc_mock_imports = ["annotationlib"]
#!SECTION - Options for Autodoc

#SECTION - Function for Autosummary
from mermaid_decision import create_mermaid_decision_maker # pyright: ignore[reportMissingImports]
#!SECTION - Function for Autosummary

#SECTION - Options for Autosummary 
autosummary_generate = True
autosummary_generate_overwrite = True
autosummary_imported_members = False
autosummary_ignore_module_all = True
autosummary_context = {}

inherit_diagramm: list[str] = [
    "ftwpki.user.cli_parser",
    "ftwpki.user.protocols",
]
exclude_inherit_diagramm: list[str] = []

class_extention_context = {
    "class_inc": "classinc",
    "module_inc": "moduleinc",
    "function_inc": "funcinc",
    "class_show_inheritance": True,
    "excl_class_show_inheritance": [
        "LineLike",
    ],
    "excl_class_show_inheritance_member": {
        "LineLike": [],
    },
    "include_private_members": {
        "LineLike": [
            "_color_map",
        ],
    },
    "autoclass_toc": True,
    "inheritence_diagram": create_mermaid_decision_maker(
        inherit_diagramm, exclude_inherit_diagramm
    ),
}

autosummary_context.update(class_extention_context)
#!SECTION - Options for Autosummary 

#!SECTION - Autodoc / Autosummary configuration -------------------------------------


#SECTION - Options for Documentationcoverage
coverage_statistics_to_stdout = True
coverage_show_missing_items = True
coverage_modules = [
    "ftwpki.user",
]

# NOTE - This list uses REGULAR EXPRESSIONS, not shell-style globs.
# Matches are performed against the Python dot notation of the modules.
# Remember to escape dots (e.g., '\.') if you want to match a literal dot.
coverage_ignore_modules = [
    r".*_version",
]
#!SECTION - Options for Documentationcoverage

#SECTION - Options for (Python) domain
add_module_names = False
python_display_short_literal_types = True
#!SECTION - Options for (Python) domain

if __name__ == "__main__":
    from typing import Any
    exclude=["os", "sys","Any","Callable", "Path" ]
    print("#"*10,"Summarized Configuration", "#"*10)
    loc=[x for x in locals().items() if x[0] not in exclude and not x[0].startswith("__")]
    def show_config(key:str, value:Any, indent:int=0) :
        indstr="    "*indent
        print(f"{indstr}{key}",end=": ")
        if isinstance(value, Callable):
            print(f"{value.__name__}()")
        elif isinstance(value,list):
            if not value:
                print("[]")
            else:
                print("[")
                ind_bracket=indstr*2 if len(indstr) > 0 else "    "
                for list_v in value:
                    list_v = f"'{list_v}'" if isinstance(list_v, str) else list_v
                    if isinstance(list_v, dict):
                        print(f"{ind_bracket}{{")
                        for lk, lv in list_v.items():
                            show_config(lk,lv,indent +2)
                        print(f"{ind_bracket}}},")
                    else:
                        print(f"{ind_bracket}{list_v},")
                    
                print(f"{ind_bracket}]")
        elif isinstance(value, dict):
            ind_braces=indstr if len(indstr) > 0 else "    "
            print("{")
            d_list = [x for x in value.items()]
            for k1, v1 in d_list:
                show_config(k1,v1,indent +1)
            print(f"{ind_braces}}},")
            return
        elif isinstance(value, (str,int,float)):
            print(value)
        else:
            print(value)
        return

    for k,v in loc:
        show_config(k,v)
