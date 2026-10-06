#!/usr/bin/env bash
# Regenerate the keymap images in draw/ with keymap-drawer.
#
# Requires keymap-drawer (Python >= 3.12):  pip install keymap-drawer==0.23.0
#
# Draws every config/cradio*.keymap, i.e. one image per firmware variant:
# draw/<name>.svg, a one-page overview in which the corners of every key show
# its other layers, plus a combos diagram.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cfg="$root/draw/config.yaml"
layout="draw/cradio_layout.json"  # key positions (Cradio/Sweep with straight thumbs)

# The keymaps include headers from ZMK modules. Reuse a west checkout if there
# is one (modules/zmk/*), otherwise fetch the revision pinned in config/west.yml.
revision="$(sed -n 's/^ *revision: *\([^ #]*\).*/\1/p' "$root/config/west.yml" | head -1)"
for module in helpers auto-layer; do
    dir="$root/modules/zmk/$module"
    if [[ ! -d "$dir" ]]; then
        git -c advice.detachedHead=false clone -q --depth 1 -b "$revision" "https://github.com/urob/zmk-$module" "$dir"
    fi
done

cd "$root"  # zmk_additional_includes in draw/config.yaml are relative to here
for keymap in config/cradio*.keymap; do
    name="$(basename "$keymap" .keymap)"
    echo "Drawing $name..."
    # Parse; combos go on their own "Combos" diagram instead of on every
    # layer (draw_overview.py handles combos that exist on a single layer).
    keymap -c "$cfg" parse -z "$keymap" --virtual-layers Combos |
        python3 -c 'import sys, yaml
km = yaml.safe_load(sys.stdin)
km["layout"] = {"qmk_info_json": sys.argv[1]}
for combo in km.get("combos", []):
    if len(combo.get("l", [])) != 1:
        combo["l"] = ["Combos"]
yaml.safe_dump(km, sys.stdout, allow_unicode=True, sort_keys=False)' "$layout" >"draw/$name.yaml"

    # One-page overview: other layers in the key corners, plus combos.
    # The parsed draw/<name>.yaml stays as a text version of every layer.
    python3 scripts/draw_overview.py "draw/$name.yaml" >"draw/${name}_overview.yaml"
    keymap -c "$cfg" draw "draw/${name}_overview.yaml" >"draw/$name.svg"
    rm "draw/${name}_overview.yaml"
    sed -i '/<text.*class="label"/d' "draw/$name.svg"  # no layer titles, like the original
done
