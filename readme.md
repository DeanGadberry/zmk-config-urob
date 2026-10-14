# Dean's Cradio keymap

My [ZMK](https://zmk.dev) firmware configuration for a **Cradio** (34-key split
keyboard, Ferris Sweep layout) with **nice!nano v2** controllers, used over
Bluetooth. It started in January 2024 as a fork of
[urob's zmk-config](https://github.com/urob/zmk-config) and has since been
reshaped around my own layout: QWERTY with home-row mods, symbol combos, and a
10-key numpad under the right hand.

![Keymap](draw/cradio.svg)

## Reading the keymap image

The big legend on each key is what it types on the base layer; the small text
underneath is its hold action (e.g. `Ctrl`, `Nav`). The corners show what the
same key does on the other layers:

| Corner | Layer | How to reach it | Color |
| --- | --- | --- | --- |
| top left | Fn | hold `Spc` | teal |
| top right | Nav | hold `Enter` | yellow |
| bottom left | Num | `Smart-num` (tap or hold) | orange |
| bottom right | Sys | hold `Smart-num`, then also `Spc` | green |

The lower diagram shows the combos (press the keys underneath at the same
time). Orange combos only exist on the Num layer.

**Printable version:** [`draw/cradio-print.pdf`](draw/cradio-print.pdf) is black
and white on letter paper, best printed double-sided: page 1 is the overview
above with a keycap legend, page 2 draws every layer separately with the key you
hold to reach each layer greyed out.

## Two keymaps

The keyboard has two independent keymaps, each built as its own firmware:

| Keymap | Files | Num layer | Firmware |
| --- | --- | --- | --- |
| **primary** | `config/base.keymap`, `config/combos.dtsi` | 10-key numpad under the right hand | `cradio_{left,right}-nice_nano_v2-zmk.uf2` |
| **legacy** | `config/legacy.keymap`, `config/combos_legacy.dtsi` | the earlier layout, numpad under the left hand | `cradio_{left,right}-nice_nano_v2-cradio_legacy-zmk.uf2` |

Everything below describes the primary keymap; the legacy one differs only in
its Num layer and combos ([`draw/cradio_legacy.svg`](draw/cradio_legacy.svg),
[`draw/cradio_legacy-print.pdf`](draw/cradio_legacy-print.pdf)).

## Layers

**Base:** QWERTY.

- **Home-row mods:** hold `A` `S` `D` `F` for Gui, Alt, Ctrl, Shift, and `J` `K`
  `L` `'` for Shift, Ctrl, Alt, Gui.
- **Thumbs:**
  - `Enter` (hold: Nav).
  - `Spc` (hold: Fn). Shift + `Spc` types `.`, a space and a one-shot Shift, to
    end a sentence.
  - `Smart-num`: the Num layer, see below.
  - `Smart-shift`: tap for a one-shot Shift, Shift + tap (or double-tap) for
    Caps Word.
- **Shifted punctuation:** Shift turns `,` into `;`, `.` into `:` and `?` into
  `!`. Ctrl + Shift turns `,` and `.` into `<` and `>`.

**Nav (hold `Enter`):**

- **Arrows:** vim-style on `H` `J` `K` `L`. Holding them gives Home, End and the
  start/end of the document instead of repeating.
- **Editing:** Backspace and Delete delete a whole word when held. Also PgUp,
  PgDn, Ins and Tab.
- **Left hand:** one-shot Gui, Alt, Ctrl and Shift, and `PWin`/`NWin`, an Alt-Tab
  window switcher that stays open while you tap.
- **Thumb:** `Exit` turns off num-word and Caps Word.

**Fn (hold `Spc`):**

- **Function keys:** F1–F12 on the left hand, laid out like a numpad.
- **Media:** previous/next track, volume, mute, play/pause.
- **Windows:** previous/next virtual desktop (`PDesk`/`NDesk`), pin an app or
  window to all desktops (`PinA`/`PinW`), the desktop switcher (`Dsk`), and
  `Sleep`.

**Num (`Smart-num`, right inner thumb):**

```
   /   7   8   9   -
   *   4   5   6   +        7 + 8 together: Backspace
   =   1   2   3   .
         [Exit] [ 0 ]       right thumbs
```

- **Tap `Smart-num` (num-word):** the layer stays on while you type digits,
  `. , + - * / =`, Enter, Backspace or Delete, and turns off with any other key
  (that key still types). There is no time limit. Press the `Smart-num` key
  (`Exit`) to leave without typing anything.
- **Hold `Smart-num`:** the layer is on only while held.
- **Double-tap `Smart-num`:** the layer is on for one key.
- **Enter** stays available from the left thumb. While the numpad is on, the
  right-hand symbol combos are switched off so they can't misfire.

**Sys (hold `Smart-num`, then also hold `Spc`):** the order matters, because
holding `Spc` first turns the `Smart-num` key into Mute.

| Key | Action |
| --- | --- |
| Q · W · E · R | Bluetooth device 1 · 2 · 3 · 4 |
| T | Bluetooth clear: forget the pairing of the current device |
| G / H | Bootloader for flashing (left / right half) |
| B / N | Restart (left / right half) |

## Combos

Press the two keys together. Most of them require a short pause (150 ms) since
the last key, so they don't misfire while you type words.

| Combo | Result | Combo | Result |
| --- | --- | --- | --- |
| `W`+`E` | Esc | `U`+`I` | Backspace |
| `E`+`R` | Enter | `I`+`O` | Delete |
| `S`+`D` | Tab | `J`+`K` | `(` (Nav: `<`) |
| `D`+`F` | Caps Lock | `K`+`L` | `)` (Nav: `>`) |
| `X`+`C` | Copy | `M`+`,` | `[` (Nav: `{`) |
| `C`+`V` | Paste | `,`+`.` | `]` (Nav: `}`) |
| `X`+`V` | Cut | | |

Vertical combos (a key and the one below it) give the number-row symbols:

| Hand | Top + home row | Home + bottom row |
| --- | --- | --- |
| left | `W` `@` · `E` `#` · `R` `$` · `T` `%` | `S` `` ` `` · `D` `\` · `F` `=` · `G` `~` |
| right | `Y` `^` · `U` `+` · `I` `*` · `O` `&` | `H` `_` · `J` `-` · `K` `/` · `L` `\|` |

(Each entry names the upper key of the pair, e.g. `W` `@` means `W` + `S`, and
`S` `` ` `` means `S` + `X`.)

## Flashing new firmware

Do this after changing the keymap (or to update ZMK). Each half is flashed
separately over USB.

**1. Download the firmware.** On GitHub go to **Actions → Build ZMK firmware**,
open the latest run on `main` and download **firmware** at the bottom of the
page. Unzip it. The primary keymap uses `cradio_left-nice_nano_v2-zmk.uf2` and
`cradio_right-nice_nano_v2-zmk.uf2`.

**2. Plug the left half in with USB and put it in bootloader mode,** either:

- **with the keymap:** hold **Smart-num** first, *then* also hold **Spc**, then
  tap **G** (`H` for the right half; each Boot key only affects its own half).
- **with the reset button:** double-tap it quickly (about half a second apart; a
  single tap just restarts the keyboard). Without a button, briefly touch the
  nice!nano's **RST** and **GND** pads together twice with tweezers.

**3. Copy the file.** A USB drive named **NICENANO** appears within a few
seconds (Mac: Finder sidebar under *Locations*; Windows: File Explorer → *This
PC*; Linux: file manager sidebar or `/media/<user>/NICENANO`). Drag the left
`.uf2` file onto it. The drive disappears on its own when done; an "ejected
improperly" warning is normal.

**4. Repeat for the right half** with the right-hand file.

**If NICENANO doesn't show up:** use a data cable (many are charge-only),
double-tap faster, plug straight into the computer instead of a hub or dock, and
make sure the half in bootloader mode is the one plugged in.

**If the halves won't connect or Bluetooth misbehaves:** flash
`settings_reset-nice_nano_v2-zmk.uf2` (also in the download) to both halves,
which clears stored pairings, then flash the normal firmware again, then remove
the keyboard from the computer's Bluetooth settings and pair it fresh.

## Changing the keymap

1. **Edit** `config/base.keymap` (layers and behaviors) or `config/combos.dtsi`
   (combos), or the legacy files.
2. **Commit and push to `main`.** Two GitHub Actions run automatically:
   - **Build ZMK firmware** builds all firmware files into one `firmware`
     download.
   - **Draw keymaps** redraws `draw/*.svg` and the printable PDFs and commits
     them, so the pictures always match the firmware.
3. **Flash** both halves as described above.

| Path | What it is |
| --- | --- |
| `config/cradio.keymap`, `config/cradio_legacy.keymap` | Entry points: one per firmware variant |
| `config/base.keymap`, `config/combos.dtsi` | Primary keymap and its combos |
| `config/legacy.keymap`, `config/combos_legacy.dtsi` | Legacy keymap and its combos |
| `config/cradio.conf` | Settings shared by both: sleep after 30 min, Bluetooth |
| `config/west.yml` | ZMK version and modules |
| `build.yaml` | Which firmware files to build |
| `.github/workflows/` | The build and drawing Actions |
| `draw/` | Keymap images, printable PDFs, drawing settings |
| `scripts/draw.sh` | Redraws the images locally (Python 3.12+, `pip install keymap-drawer==0.23.0`; the PDFs also need Chrome or Chromium) |

**Firmware version:** official ZMK **v0.3**, plus three of urob's modules pinned
to the same release in `config/west.yml`:
[zmk-helpers](https://github.com/urob/zmk-helpers) (keymap macros),
[zmk-auto-layer](https://github.com/urob/zmk-auto-layer) (num-word) and
[zmk-tri-state](https://github.com/urob/zmk-tri-state) (the Alt-Tab switcher).
The build uses a copy of ZMK's own v0.3 workflow
(`.github/workflows/build-user-config.yml`), updated only for current GitHub
action versions and pinned runner/container images. To upgrade, change every
`v0.3` in `config/west.yml` to the next ZMK release and refresh that workflow
copy from the same release (the note at its top lists what was changed).

To add another keymap variant, copy `cradio_legacy.keymap` and `legacy.keymap`
under a new name and add matching entries to `build.yaml` with
`cmake-args: -DKEYMAP_FILE=${GITHUB_WORKSPACE}/config/<name>.keymap` and an
`artifact-name`.

## Known issues

- **Sys layer order:** you have to hold Smart-num *before* Spc; the other way
  round mutes the audio.
- **Caps Word no longer turns off when you press a modifier.** That came from
  urob's old ZMK fork; official ZMK doesn't do it.
- **The `game` layer can't be reached.** It is defined in both keymaps, but no
  key switches to it yet.
- **`scripts/zmk_*.sh` and `img/` are left over from urob's config.** The Docker
  build scripts no longer match this setup, and the images are superseded by
  `draw/`.

## Credits

- [urob](https://github.com/urob/zmk-config) for the original configuration:
  "timeless" home-row mods (280 ms tapping term, balanced flavor, 150 ms
  prior-idle, same-hand keys always tap), the combo layout, num-word, the
  Alt-Tab switcher and the keymap-drawing approach. His readme explains the
  home-row mod tuning in detail.
- [ZMK](https://zmk.dev) for the firmware, and
  [keymap-drawer](https://github.com/caksoylar/keymap-drawer) for the images.
