"""Build the printable black-and-white keymap PDF for one keymap.

Page 1: one-page overview, other layers in the key corners (plain grey), with a
        keycap legend explaining the corners.
Page 2: every layer drawn separately; the key held to reach each layer is
        greyed out.

Usage: python3 draw_print.py <parsed.yaml> <out.pdf> <chrome>
Needs the `keymap` (keymap-drawer) command and a Chrome/Chromium binary.
"""

import copy
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

parsed, out_pdf, chrome = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
root = Path(__file__).resolve().parent.parent
name = parsed.stem
full = yaml.safe_load(open(parsed))
overview = yaml.safe_load(
    subprocess.run(["python3", str(root / "scripts/draw_overview.py"), str(parsed)],
                   check=True, capture_output=True, text=True).stdout
)
base_cfg = yaml.safe_load(open(root / "draw/config.yaml"))

LAYERS = ["base", "nav", "fn", "num", "sys", "Combos"]
# Key positions held to reach each layer: 30 = Enter, 31 = Spc, 32 = Smart-num.
HELD = {"nav": [30], "fn": [31], "num": [32], "sys": [31, 32]}
ACCESS = {  # corner -> (layer, how to reach it)
    "tl": ("Fn", "hold <b>Spc</b> (left thumb)"),
    "tr": ("Nav", "hold <b>Enter</b> (left thumb)"),
    "bl": ("Num", "<b>Smart-num</b>: tap = num-word, hold = while held"),
    "br": ("Sys", "hold <b>Smart-num</b>, then <b>Spc</b>"),
}

CSS = """
svg.keymap { fill: #000; background: #fff; font-family: 'Liberation Sans', Arial, sans-serif; font-size: 16px; }
svg path { fill: inherit; }
text { text-anchor: middle; dominant-baseline: middle; }
text.tap { font-weight: 600; }
text.hold { font-size: 11px; dominant-baseline: auto; }
text.shifted { font-size: 10px; dominant-baseline: hanging; }
text.tl, text.tr, text.bl, text.br, text.combo { font-size: 10px; }
text.hold, text.bl, text.br { dominant-baseline: auto; }
text.shifted, text.tl, text.tr { dominant-baseline: hanging; }
text.tl, text.bl { text-anchor: start; }
text.tr, text.br { text-anchor: end; }
text.tl, text.tr, text.bl, text.br, use.tl, use.tr, use.bl, use.br { fill: #555; }
text.label { display: none; }
text.footer { display: none; }
rect.key { fill: #fff; stroke: #000; stroke-width: 1.2; }
rect.held { fill: #b8b8b8; }
rect.combo, rect.combo-separate { fill: #fff; stroke: #000; stroke-width: 1; }
.layer-Combos rect.key { fill: #fff; stroke: #bbb; stroke-dasharray: 3 2; }
path.combo { stroke: #888; stroke-width: 1; stroke-dasharray: 2 2; fill: none; }
rect.combo.num { fill: #000; } rect.combo.num + text { fill: #fff; }
"""

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: letter landscape; margin: 0.45in; }}
body {{ margin: 0; font-family: 'Liberation Sans', Arial, sans-serif; color: #000; background: #fff; }}
section {{ break-after: page; }} section:last-child {{ break-after: auto; }}
h1 {{ font-size: 14pt; margin: 0 0 4pt; }}
.svg img {{ width: 100%; height: auto; object-fit: contain; display: block; }}
.p1 .svg img {{ max-height: 5.6in; }} .p2 .svg img {{ max-height: 6.55in; }}
.legend {{ font-size: 9.5pt; border: 0.75pt solid #000; padding: 4pt 6pt; margin-top: 4pt; }}
.lg {{ display: grid; grid-template-columns: 1fr auto 1fr; grid-template-rows: auto auto; column-gap: 10pt; align-items: center; }}
.lg .cap {{ grid-column: 2; grid-row: 1 / span 2; height: 1.15in; }}
.lg .tl, .lg .bl {{ grid-column: 1; text-align: right; }} .lg .tr, .lg .br {{ grid-column: 3; text-align: left; }}
.lg .tl, .lg .tr {{ grid-row: 1; align-self: start; padding-top: 6pt; }}
.lg .bl, .lg .br {{ grid-row: 2; align-self: end; padding-bottom: 6pt; }}
.note {{ margin-top: 3pt; text-align: center; color: #333; }}
.swatch {{ display: inline-block; width: 12pt; height: 9pt; background: #b8b8b8; border: 0.75pt solid #000;
           border-radius: 2pt; vertical-align: -1pt; }}
</style></head><body>
<section class="p1"><h1>{title} — overview</h1><div class="svg"><img src="overview.svg"></div>
<div class="legend"><div class="lg">{cells}</div>
<div class="note">Black combos (<b>=</b> and <b>Bspc</b>) only work on the Num layer.</div></div></section>
<section class="p2"><h1>{title} — every layer</h1><div class="svg"><img src="layers.svg"></div>
<div class="legend"><span class="swatch"></span> grey key = the key you hold to reach that layer
(Sys: hold Smart-num, then Spc).</div></section>
</body></html>"""


def draw(km, cfg_updates, path):
    cfg = copy.deepcopy(base_cfg)
    cfg["draw_config"].update({"footer_text": "", "svg_style": CSS, **cfg_updates})
    cfg_path, km_path = path.with_suffix(".config.yaml"), path.with_suffix(".keymap.yaml")
    yaml.safe_dump(cfg, open(cfg_path, "w"), allow_unicode=True, sort_keys=False)
    yaml.safe_dump(km, open(km_path, "w"), allow_unicode=True, sort_keys=False)
    svg = subprocess.run(["keymap", "-c", str(cfg_path), "draw", str(km_path)],
                         check=True, capture_output=True, text=True).stdout
    path.write_text(svg)


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    draw(overview, {}, tmp / "overview.svg")

    # Page 2: every layer, held keys greyed out and labelled with the base key.
    layers = copy.deepcopy(full)
    base = layers["layers"]["base"]
    for layer, positions in HELD.items():
        for pos in positions:
            key = layers["layers"][layer][pos]
            label = base[pos] if isinstance(base[pos], str) else base[pos].get("t", "")
            current = key if isinstance(key, str) else key.get("t", "")
            if current and current != label and not (isinstance(key, dict) and key.get("type") == "trans"):
                layers["layers"][layer][pos] = {"t": current, "h": label, "type": "held"}  # e.g. "0" on Smart-num
            else:
                layers["layers"][layer][pos] = {"t": label, "type": "held"}
    layers["layers"] = {n: layers["layers"][n] for n in LAYERS if n in layers["layers"]}
    layers["combos"] = [c for c in layers.get("combos", []) if all(l in layers["layers"] for l in c.get("l", []))]
    draw(layers, {"n_columns": 2}, tmp / "layers.svg")
    (tmp / "layers.svg").write_text(
        (tmp / "layers.svg").read_text().replace(
            "text.label { display: none; }",
            "text.label { display: inline; font-weight: 700; font-size: 14px; text-anchor: start; }"))

    # Legend keycap: one key with the layer names in their corners.
    cap = {"layout": {"ortho_layout": {"split": False, "rows": 1, "columns": 1, "thumbs": 0}},
           "layers": {"Legend": [{"t": "Letter", "h": "hold", **{c: ACCESS[c][0] for c in ACCESS}}]}}
    draw(cap, {"key_w": 96, "key_h": 72, "n_columns": 1}, tmp / "legend.svg")
    cells = "".join(
        (f'<div class="c {c}"><b>{ACCESS[c][0]}</b> — {ACCESS[c][1]}</div>'
         + ('<img class="cap" src="legend.svg">' if c == "tl" else ""))
        for c in ("tl", "tr", "bl", "br")
    )

    title = {"cradio": "Cradio keymap (primary)", "cradio_legacy": "Cradio keymap (legacy)"}.get(name, name)
    (tmp / "page.html").write_text(PAGE.format(title=title, cells=cells))
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out_pdf.resolve()}", f"file://{tmp}/page.html"],
                   check=True, capture_output=True)

# Fixed timestamps (same length, so the PDF's byte offsets stay valid): an
# unchanged keymap then produces a byte-identical PDF and no spurious commits.
pdf = out_pdf.read_bytes()
pdf = re.sub(rb"\((D:\d{14}[^)]*)\)", lambda m: b"(" + b"D:20000101000000" + m.group(1)[16:] + b")", pdf)
out_pdf.write_bytes(pdf)
print("wrote", out_pdf)
