"""Build the one-page overview keymap from a parsed keymap-drawer YAML.

Every key of the base layer also shows what it does on the other layers, in its
corners: fn top-left, nav top-right, num bottom-left, sys bottom-right. Combos
active on several layers get their own diagram. Adapted from the `draw` recipe
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
# Single-layer combos (e.g. "=" on the num layer) only make sense on their own
# layer, which isn't drawn here; they appear in the per-layer image instead.
km["combos"] = [c for c in km.get("combos", []) if c.get("l") == ["Combos"]]

yaml.safe_dump(km, sys.stdout, allow_unicode=True, sort_keys=False)
