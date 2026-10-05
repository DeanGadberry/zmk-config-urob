#!/usr/bin/env bash
# Regenerate the keymap images in draw/ with keymap-drawer.
#
# Requires keymap-drawer (Python >= 3.12):  pip install keymap-drawer==0.23.0
#
# Draws every config/cradio*.keymap, i.e. one image per firmware variant:
# draw/cradio.svg, draw/cradio_alt.svg, ...
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cfg="$root/draw/config.yaml"
keyboard="cradio"  # physical layout for every variant (keymap-drawer ZMK shield name)

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
    # Draw all combos on their own "Combos" diagram instead of on every layer.
    keymap -c "$cfg" parse -z "$keymap" --virtual-layers Combos |
        python3 -c 'import sys, yaml
km = yaml.safe_load(sys.stdin)
for combo in km.get("combos", []):
    combo["l"] = ["Combos"]
yaml.safe_dump(km, sys.stdout, allow_unicode=True, sort_keys=False)' >"draw/$name.yaml"
    keymap -c "$cfg" draw -z "$keyboard" "draw/$name.yaml" >"draw/$name.svg"
done
