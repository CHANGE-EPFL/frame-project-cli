# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

import os
import sys
from datetime import datetime

import frame_cli

# -- Project information

project = "FRAME CLI"

copyright = f"2024-{datetime.now().year} EPFL (École Polytechnique Fédérale de Lausanne)"
author = "Son Pham-Ba"
__version__ = frame_cli.__version__
version = __version__
release = __version__

# -- General configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "myst_parser",
]


templates_path = ["_templates"]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": True,
}

# -- Options for HTML output

html_theme = "press"
html_theme_options = {
    "external_links": [
        ("FRAME Library", "https://frame-dev.epfl.ch"),
        ("GitHub", "https://github.com/CHANGE-EPFL/frame-project"),
    ]
}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["custom.js"]

# -- Options for MyST

myst_heading_anchors = 3

# -- Options for EPUB output
epub_show_urls = "footnote"


# -- Automatically run apidoc to generate rst from code
# https://github.com/readthedocs/readthedocs.org/issues/1139
def run_apidoc(_) -> None:
    from sphinx.ext.apidoc import main

    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    cur_dir = os.path.abspath(os.path.dirname(__file__))

    for module_dir in [
        "frame_cli",
    ]:
        module = os.path.join(cur_dir, "..", module_dir)
        output = os.path.join(cur_dir, "auto_source", module_dir)
        main(["-e", "-f", "-o", output, module])


def setup(app) -> None:
    app.connect("builder-inited", run_apidoc)
