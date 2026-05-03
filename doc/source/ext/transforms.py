"""
Transforms and event handlers for document tree manipulation. (rw)

To use these transforms, add the following to your conf.py setup(app) function:
    app.connect("doctree-read", inject_option_anchors)
    app.add_transform(InjectArgparseAnchors)
"""
from docutils import nodes
from sphinx.transforms import SphinxTransform

def inject_option_anchors(app, doctree):
    """
    Event handler: Scans the doctree for option_list_items and injects 
    anchors based on the first option string found.
    """
    docname = app.env.docname
    std = app.env.get_domain("std")

    for node in doctree.traverse(nodes.option_list_item):
        if len(node) < 1 or not isinstance(node[0], nodes.option_group):
            continue

        option_nodes = list(node[0].traverse(nodes.option_string))
        if not option_nodes:
            continue

        opt_text = option_nodes[0].astext()
        anchor_id = f"opt-{opt_text}"

        if anchor_id not in node["ids"]:
            node["ids"].append(anchor_id)

        # Register the anchor as a label for internal linking
        std.data["labels"][anchor_id] = (docname, anchor_id, opt_text)

class InjectArgparseAnchors(SphinxTransform):
    """
    Transform: Injects unique IDs into all option_group nodes to allow 
    direct linking via the :ftwoption: role.
    """
    default_priority = 10

    def apply(self, **kwargs) -> None:
        std = self.env.get_domain("std")
        docname = self.env.docname

        for node in self.document.findall(nodes.option_group):
            option_nodes = list(node.findall(nodes.option_string))
            if not option_nodes:
                continue

            # Identify the primary option (longest string) for the main ID
            primary_opt = max([n.astext() for n in option_nodes], key=len)
            clean_id = nodes.make_id(f"opt-{primary_opt}")

            if clean_id not in node["ids"]:
                node["ids"].append(clean_id)

            # Register all variants of the option as labels
            for opt_node in option_nodes:
                opt_text = opt_node.astext().strip()
                label_key = f"opt-{opt_text}"
                std.data["labels"][label_key] = (docname, clean_id, opt_text)
