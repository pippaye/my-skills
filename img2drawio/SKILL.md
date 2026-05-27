---
name: img2drawio
description: Convert structured diagram images, flowcharts, architecture diagrams, UI sketches, schematics, and similar visual references into faithful, editable draw.io .drawio XML files. Use when the user asks to convert an image to draw.io, redraw a diagram as draw.io, make an image editable in draw.io, generate .drawio from a screenshot, or create an editable diagram from an uploaded image. Do not use for photos or continuous-tone artwork unless the user explicitly accepts a coarse diagrammatic redraw.
---

# Image to Draw.io

Convert a structured image into an editable draw.io diagram. The output must be a faithful redraw using native draw.io shapes, text, and connectors, not a whole-image bitmap embed.

## Core Rules

- Measure from the image; do not invent layout, colors, text, or relationships.
- Use `WORKDIR="$(mktemp -d)"` for every invocation and write all generated artifacts there.
- Never write to hardcoded paths such as `/home/claude`, `/mnt/user-data/outputs`, or repo-specific output folders.
- Always deliver these files: `$WORKDIR/output.py`, `$WORKDIR/output.drawio`, `$WORKDIR/output.png`.
- `$WORKDIR/output.py` is per-image runtime output. It must contain editable style tokens in `CONFIG`, XML template strings, and generation functions.
- The skill source tree must stay read-only during normal use; do not create per-image `output.py` in the skill directory.
- Force Arial for all text: every text-bearing draw.io style must include `fontFamily=Arial`.
- Use uncompressed `.drawio` XML, not compressed diagram payloads.
- Export PNG previews directly with `drawio` or `draw.io` CLI; do not use a Python wrapper.
- Use multimodal inspection for visual comparison by default. Pixel-level diff is optional and off by default.

## Workflow

1. Create a temporary workspace:

   ```bash
   WORKDIR="$(mktemp -d)"
   ```

2. Inspect the source image:

   ```bash
   python <skill-dir>/scripts/inspect_image.py <image>
   ```

   Use `--point X Y` or `--region X0 Y0 X1 Y1` for uncertain colors. Read `references/image-measurement.md` when coordinate, color, text, or connector measurement is non-trivial.

3. View the source image. Build an element inventory before writing XML. This inventory is for planning the template, not for dumping every element into `CONFIG`:

   - Page size and background.
   - Shapes: `id`, label text, `x`, `y`, `width`, `height`, shape type, fill color, stroke color, stroke width, font size, bold/italic flags.
   - Connectors: source id, target id, edge route, exit/entry side or point, waypoints, arrowheads, stroke color, stroke width.
   - Standalone text labels.

4. Generate `$WORKDIR/output.py`. It must:

   - Define a small top-level `CONFIG` dictionary that acts like CSS variables: shared colors, font sizes, stroke widths, spacing, and named style tokens.
   - Keep diagram structure in XML template strings, not in `CONFIG`.
   - Keep per-element ids, text, coordinates, parent/source/target relationships, and waypoints in the template string where the XML structure is visible.
   - Use placeholders such as `{process_style}`, `{edge_style}`, `{panel_fill}`, `{font_family}`, and `{accent_stroke}` to apply shared style tokens from `CONFIG`.
   - Extract repeated draw.io style strings into named style variables/functions built from `CONFIG`, similar to CSS classes.
   - Escape XML attribute values correctly.
   - Write `$WORKDIR/output.drawio` when run.
   - Make style tuning user-friendly: the user should usually edit 10-20 style variables in `CONFIG`, not a giant list of shape dictionaries.
   - Do not move XML complexity into a huge `CONFIG`; if `CONFIG` starts looking like serialized HTML/XML, the design is wrong.

5. Run the generator and validate the output:

   ```bash
   python "$WORKDIR/output.py"
   python <skill-dir>/scripts/validate_drawio.py "$WORKDIR/output.drawio" <skill-dir>/references/mxfile.xsd
   ```

6. Export the PNG preview directly with draw.io CLI. Probe wrapper behavior instead of assuming one packaging layout:

   ```bash
   DRAWIO_BIN="$(command -v drawio || command -v draw.io)"
   test -n "$DRAWIO_BIN"

   rm -f "$WORKDIR/output.png"
   "$DRAWIO_BIN" -x -f png -o "$WORKDIR/output.png" "$WORKDIR/output.drawio" || true

   if [ ! -s "$WORKDIR/output.png" ]; then
     # Nix/NixOS wrappers may inject Ozone/Wayland flags before the input file.
     # Keep using the wrapper, but remove that wrapper-specific injection trigger.
     env -u NIXOS_OZONE_WL "$DRAWIO_BIN" -x -f png -o "$WORKDIR/output.png" "$WORKDIR/output.drawio" || true
   fi

   if [ ! -s "$WORKDIR/output.png" ]; then
     # Last resort for shell wrappers that exec Electron with an app.asar.
     WRAPPER="$(readlink -f "$DRAWIO_BIN")"
     ELECTRON_BIN="$(sed -n 's/.*"\([^"]*electron[^"]*\/bin\/electron\)".*/\1/p' "$WRAPPER" | head -n 1)"
     APP_ASAR="$(sed -n 's/.*electron"  \([^ ]*app\.asar\).*/\1/p' "$WRAPPER" | head -n 1)"
     if [ -n "$ELECTRON_BIN" ] && [ -n "$APP_ASAR" ]; then
       "$ELECTRON_BIN" "$APP_ASAR" -x -f png -o "$WORKDIR/output.png" "$WORKDIR/output.drawio" || true
     fi
   fi

   test -s "$WORKDIR/output.png"
   ```

   If `DRAWIO_BIN` is empty, stop and report that draw.io CLI is required. Some draw.io desktop wrappers print an error while still exiting with status 0, so always verify that `$WORKDIR/output.png` exists and is non-empty after export.

7. Use multimodal inspection to compare the source image and `$WORKDIR/output.png`.

8. If issues remain, edit `$WORKDIR/output.py`, regenerate, validate, export, and inspect again. Use `CONFIG` for broad style tuning; edit the template string for structural fixes such as coordinates, labels, source/target links, or waypoints. Run at most 3 repair rounds unless the user asks for more.

9. Optional pixel-diff mode. Run this only when the user explicitly asks for pixel-level diff output, or when a stricter debugging pass is worth extra artifacts:

   ```bash
   python <skill-dir>/scripts/compare_pixels.py <source-image> "$WORKDIR/output.png" "$WORKDIR/pixel_diff"
   ```

   This writes `$WORKDIR/pixel_diff_side.png`, `$WORKDIR/pixel_diff_overlay.png`, and `$WORKDIR/pixel_diff_diff.png`, and prints `mean_pixel_error`. These files are diagnostic artifacts, not required deliverables.

10. Final response must report the three deliverables:

   - `$WORKDIR/output.py`
   - `$WORKDIR/output.drawio`
   - `$WORKDIR/output.png`

## Draw.io XML Requirements

The generated `.drawio` must use native editable cells:

- Root structure: `mxfile > diagram > mxGraphModel > root`.
- Required root cells:
  - `<mxCell id="0"/>`
  - `<mxCell id="1" parent="0"/>`
- Shapes and text are `mxCell` elements with `vertex="1"` and `parent="1"`.
- Connectors are `mxCell` elements with `edge="1"`, `parent="1"`, `source`, and `target`.
- Each vertex has an `mxGeometry` child with `x`, `y`, `width`, `height`, and `as="geometry"`.
- Each edge has an `mxGeometry` child with `relative="1"` and `as="geometry"`.
- Use `mxPoint` children for edge waypoints when needed.
- Do not embed the whole source image as an `image=data:image/...` cell.

Use `references/style-reference.md` for draw.io style vocabulary and `references/mxfile.xsd` for schema validation.

## Measurement Rules

Inline mandatory rules:

- Use the source image pixel dimensions as the page reference.
- Read coordinates from the source image using visual inspection and image dimensions; do not estimate from memory.
- Sample colors from the image with `--point` or `--region` when unsure.
- Transcribe text exactly, including case, punctuation, and line breaks.
- Use Arial even if the source font differs.
- Preserve approximate proportions, grouping, visual hierarchy, stroke widths, and arrow directions.
- Anchor connectors to shape boundaries; arrows must not float in whitespace or overshoot into unrelated shapes.
- Use orthogonal routes and waypoints when the source uses elbow connectors.

Detailed techniques live in `references/image-measurement.md`.

## Preview Repair Checklist

After exporting `$WORKDIR/output.png`, inspect it against the source image:

- Missing or extra elements.
- Wrong coordinates, dimensions, or proportions.
- Colors not sampled from the source image.
- Incorrect, missing, clipped, or misaligned text.
- Arrows not attached to the correct shape boundaries.
- Connectors crossing through unrelated shapes when the source avoids them.
- Overlapping shapes or labels.
- Off-canvas content.
- Wrong layer order.
- Any whole-image bitmap substitution.

Targeted repair rules:

- Single shape position/size issue: edit the affected `mxGeometry` in the template string.
- Wrong shared color, stroke, font size, or spacing: edit the named style token in `CONFIG`.
- One-off color or stroke exception: use a local template placeholder or literal only when it is visibly unique in the source image.
- Text mismatch: edit the `value` in the template string, or edit a shared font/spacing token in `CONFIG` if many labels are affected.
- Floating connector: adjust source/target, exit/entry style, or waypoints in the template string.
- Widespread layout mismatch: update the measured template structure, but keep the same deliverable filenames.
- Invalid XML or validation failure: fix `$WORKDIR/output.py` generation logic first, then regenerate.

Stop after 3 repair rounds unless the user asks for further refinement.

## Optional Pixel-Diff Mode

Default behavior is multimodal inspection only. Do not generate pixel diff files unless requested.

Use `scripts/compare_pixels.py` when exact visual drift needs debugging. It is useful for spotting large shifts, missing blocks, and color mismatches, but the numeric score is only a guide because draw.io text rendering, anti-aliasing, and shape metrics may differ from the source image even when the editable diagram is acceptable.
