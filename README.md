# Pin Forge

[Русская версия](README.ru.md)

Turn an SVG logo into a printable lapel pin: a binary STL, or a ready-made
Orca/Bambu project with the print profile already baked in. Everything is
computed in the browser. The file never leaves your machine.

The interface is bilingual, English and Russian, with a switch in the header.

## Running it

Open `index.html` in a browser. The libraries live in `vendor/`, so no
internet connection is required.

If your browser blocks local files, which happens with some settings:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## What is in the repository

| File | What it is |
|---|---|
| `index.html` | the whole generator: markup, styles, logic |
| `vendor/three.min.js` | three.js r128, preview and geometry |
| `vendor/pako.min.js` | deflate for zip and 3mf compression |

There is no build step and no transpilation. You edit the file directly.

## SVG requirements

- text converted to outlines
- strokes converted to filled paths (Illustrator: Object → Path → Stroke to Path)
- no `clipPath`, no masks, no `<use>`
- shapes with a fill, not stroke-only

## How the code is laid out

Everything sits in one `<script>` at the end of `index.html`, in sections:

- **SVG parsing** — `parseSVGtoRings` samples paths through `getPointAtLength`,
  splits them into subpaths and applies the CTM. The output is arrays of points.
- **Analysis** — `analyzeLogo` casts rays along the outline normal, inward and
  outward, to measure the thinnest stroke and the narrowest gap. It draws a map
  of the places that will not print.
- **Plate outline** — `plateOutline` rasterises the letters on a canvas, inflates
  them with a round-joined stroke, which is an honest offset with no
  self-intersections, then traces back to vectors through marching squares with
  alpha interpolation. Overlapping letters merge into a single contour.
- **Geometry** — `buildPin` builds the body (disc, outline or rounded rectangle),
  the relief or engraved letters, the insert socket and the pad on the back.
- **Insert placement** — `bestSpot` looks for the point closest to the centre
  where the insert fits, searching within a central zone.
- **Export** — `toBinarySTL`, `make3MF`, `makeZip`, a hand-rolled zip writer with
  deflate and UTF-8 filenames.
- **Localisation** — `I18N` holds both dictionaries, `t()` resolves a key,
  `applyLang()` walks `data-i18n` attributes and re-renders everything dynamic.
  Russian is the complete dictionary: a key missing from English falls back to it.

## Processes

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

## Deployment

The page is static, so any web server will do. It is currently served from nginx
at [pin.gorskikh.com](https://pin.gorskikh.com).

## License

Not decided yet. Ask before reusing.
