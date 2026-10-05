#!/usr/bin/env bash
# Regenerate the keymap images in draw/ with keymap-drawer.
#
# Requires keymap-drawer (Python >= 3.12):  pip install keymap-drawer==0.23.0
# and the zmk-nodefree-config submodule:    git submodule update --init
#
# Draws every config/<name>.keymap that isn't an included sub-file, i.e. one
# image per firmware variant: draw/cradio.svg, draw/cradio_alt.svg, ...
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cfg="$root/draw/config.yaml"
keyboard="cradio"  # physical layout for every variant (keymap-drawer ZMK shield name)

for keymap in "$root"/config/cradio*.keymap; do
    name="$(basename "$keymap" .keymap)"
    echo "Drawing $name..."
    # Draw all combos on their own "Combos" diagram instead of on every layer.
    keymap -c "$cfg" parse -z "$keymap" --virtual-layers Combos |
        python3 -c 'import sys, yaml
km = yaml.safe_load(sys.stdin)
for combo in km.get("combos", []):
    combo["l"] = ["Combos"]
yaml.safe_dump(km, sys.stdout, allow_unicode=True, sort_keys=False)' >"$root/draw/$name.yaml"
    keymap -c "$cfg" draw -z "$keyboard" "$root/draw/$name.yaml" >"$root/draw/$name.svg"
done
