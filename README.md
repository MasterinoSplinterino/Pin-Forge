# Pin Forge

[Русская версия](README.ru.md)

Turn an SVG logo into a printable lapel pin: a binary STL, or a ready-made
Orca/Bambu project with the print profile already baked in. Everything is
computed in the browser and the file never leaves your machine.

## Try it

### → [pin.gorskikh.com](https://pin.gorskikh.com)

Nothing to install and nothing to sign up for. Drop an SVG under the preview
and the pin appears.

![Pin Forge: an SVG logo raised into a pin, with the print checks alongside](docs/screenshot.png)

The interface is bilingual, English and Russian, with a switch in the header.

## What it gives you

- **A body that fits the logo** — a round disc, a rounded rectangle, or a plate
  cut to the outline of the letters themselves.
- **A socket for the hardware** — butterfly clutch pin or a magnet, recessed,
  glued onto a pad, or sunk under a printed lid with a pause in the print.
- **A printability check** — the thinnest stroke and the narrowest gap are
  measured against the selected process, with a map of the spots that will not
  come out and concrete advice on how to fix them.
- **A test tile** — a 3×3 grid across logo sizes and relief heights, so one
  print tells you which combination survives.

## SVG requirements

- text converted to outlines
- strokes converted to filled paths (Illustrator: Object → Path → Stroke to Path)
- no `clipPath`, no masks, no `<use>`
- shapes with a fill, not stroke-only

## What is in the repository

| File | What it is |
|---|---|
| `index.html` | the whole generator: markup, styles, logic |
| `vendor/three.min.js` | three.js r128, preview and geometry |
| `vendor/pako.min.js` | deflate for zip and 3mf compression |

There is no build step and no transpilation. You edit the file directly.

## How the code is laid out

Everything sits in one `<script>` at the end of `index.html`, in sections:

- **SVG parsing** — `parseSVGtoRings` samples paths through `getPointAtLength`,
  splits them into subpaths and applies the CTM. The output is arrays of points.
  Uploaded files pass through `sanitizeSVG` first, because the logo is inserted
  into the document and would otherwise run whatever handlers it carries.
- **Analysis** — `analyzeLogo` casts rays along the outline normal, inward and
  outward, to measure the thinnest stroke and the narrowest gap. It draws a map
  of the places that will not print.
- **Plate outline** — `plateOutline` rasterises the letters on a canvas, inflates
  them with a round-joined stroke, which is an honest offset with no
  self-intersections, then traces back to vectors through marching squares with
  alpha interpolation. Overlapping letters merge into a single contour.
- **Geometry** — `buildPin` builds the body, the relief or engraved letters, the
  insert socket and the pad on the back.
- **Insert placement** — `bestSpot` looks for the point closest to the centre
  where the insert fits, searching within a central zone.
- **Logo centring** — `letterBandCenter` takes the median of the contour mid
  heights as the real line height, so an ascender like a `t` no longer drags the
  whole word off centre. The shift is clamped so the logo cannot leave the plate.
- **Export** — `toBinarySTL`, `make3MF`, `makeZip`, a hand-rolled zip writer with
  deflate and UTF-8 filenames.
- **Localisation** — `I18N` holds both dictionaries, `t()` resolves a key,
  `applyLang()` walks `data-i18n` attributes and re-renders everything dynamic.
  Russian is the complete dictionary: a key missing from English falls back to it.

## Processes

Every value the generator would apply is listed in the Print settings section
of the interface, with a copy button, and explained value by value in
[PRINT-SETTINGS.md](PRINT-SETTINGS.md), which is in Russian.

The minimum stroke and gap thresholds depend on the selected process (`TECH` in
the code). For FDM the generator also suggests how to tune the stroke to a whole
number of perimeters.

## 3mf export

The project carries the full print settings: layer height, Arachne, compensations,
speeds, accelerations, cooling, scarf joint. The printer profile name is written
as a plain string (`PRINTERS` in the code). If your Orca preset is named
differently, the print settings still apply and the printer stays the current one.

## Adding a language

1. Add a third key next to `ru` and `en` in `I18N`.
2. Add a button to the `.lang` group in the header with the matching `data-lang`.
3. Anything you leave out falls back to Russian.

## Running it locally

Open `index.html` in a browser. The libraries live in `vendor/`, so no internet
connection is required.

If your browser blocks local files, which happens with some settings:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploying it yourself

The page is static, so any web server or static host will serve it. Copy
`index.html` and the `vendor/` folder into a document root and point a domain at
it. There is nothing to build, no runtime and no backend.

## License

Not decided yet. Ask before reusing.
