"""Build the one-page overview keymap from a parsed keymap-drawer YAML.

Every key of the base layer also shows what it does on the other layers, in its
corners: fn top-left, nav top-right, num bottom-left, sys bottom-right. All
combos go on a second diagram. Adapted from the `draw` recipe
in urob/zmk-config's Justfile.

Usage: python3 draw_overview.py <parsed.yaml> > overview.yaml
"""

import sys

import yaml

CORNERS = {"fn": "tl", "nav": "tr", "num": "bl", "sys": "br"}


def label(key):
    """Short label of a key on an overlay layer, or None if it does nothing there."""
    if isinstance(key, dict):
        if key.get("type") in ("trans", "held"):
            return None
        key = key.get("t", "")
    return key or None


km = yaml.safe_load(open(sys.argv[1]))
layers = km["layers"]

base = []
for i, key in enumerate(layers["base"]):
    key = dict(key) if isinstance(key, dict) else {"t": key}
    for layer, corner in CORNERS.items():
        overlay = label(layers[layer][i]) if layer in layers else None
        if overlay is not None:
            key[corner] = overlay
    base.append(key)

km["layers"] = {"Base": base, "Combos": layers["Combos"]}
# All combos go on the combos diagram. Combos that only exist on one overlay
# layer (e.g. "=" on the num layer) are colored like that layer's corner.
combos = []
for combo in km.get("combos", []):
    layer = combo.get("l", ["Combos"])[0] if len(combo.get("l", [])) == 1 else "Combos"
    if layer in CORNERS:
        key = combo["k"] if isinstance(combo["k"], dict) else {"t": combo["k"]}
        combo = dict(combo, k=dict(key, type=layer))
    if not combo.get("hidden"):
        combos.append(dict(combo, l=["Combos"]))
km["combos"] = combos

yaml.safe_dump(km, sys.stdout, allow_unicode=True, sort_keys=False)
