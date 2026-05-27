# Image Measurement Reference

Use this reference when the source image requires careful coordinate, color, text, or connector reconstruction.

## Coordinate Model

Use the source image pixel dimensions as the draw.io page reference. If the image is `W x H`, treat the useful drawing area as a `W` by `H` coordinate plane. A shape measured at pixel box `(x, y, w, h)` should usually become an `mxGeometry` with the same values or a very close approximation.

For each measured box, keep these helper values:

```text
cx = x + w / 2
cy = y + h / 2
right = x + w
bottom = y + h
```

Read positions from the source image using its pixel dimensions and visual inspection. Do not infer coordinates from memory after looking at the image once.

## Color Sampling

Use source colors only.

- Use `--region X0 Y0 X1 Y1` for fill colors; sample inside the shape away from borders and text.
- Use `--point X Y` for thin strokes, lines, and arrowheads.
- Prefer uppercase `#RRGGBB` values for style tokens and template placeholders.
- Preserve real hierarchy: thick borders stay thick, light secondary lines stay light.
- Do not add gradients, shadows, or rounded corners unless they are visible in the source.

## Text

Always generate editable draw.io text, never path outlines or embedded images.

- Transcribe text exactly, including line breaks, punctuation, and case.
- Force `fontFamily=Arial` in the style.
- Match approximate font size and weight from the source.
- For text inside a shape, use the shape cell value when practical.
- For free-standing labels, create separate text vertices with `text;html=1;strokeColor=none;fillColor=none;fontFamily=Arial`.
- Increase geometry width/height when preview text is clipped.

## Connector Anchoring

Connectors must attach to the boundary of the source and target shapes. Avoid endpoints that float in whitespace.

For two axis-aligned boxes A -> B, start with these anchors:

```text
A left of B:  exit at A right edge, enter B left edge
A right of B: exit at A left edge, enter B right edge
A above B:    exit at A bottom edge, enter B top edge
A below B:    exit at A top edge, enter B bottom edge
```

In draw.io edge styles, use relative perimeter positions where useful:

```text
exitX=1;exitY=0.5;entryX=0;entryY=0.5
exitX=0.5;exitY=1;entryX=0.5;entryY=0
```

For elbow routes, add waypoints in the edge geometry:

```xml
<Array as="points">
  <mxPoint x="300" y="120"/>
  <mxPoint x="300" y="240"/>
</Array>
```

Use waypoints to match the source route and avoid crossing unrelated shapes. For parallel edges, vary entry/exit points or waypoints so labels and arrowheads remain readable.

## Shape Selection

Use native draw.io shapes that match the source:

- Process box: `rounded=0;whiteSpace=wrap;html=1`
- Rounded process box: `rounded=1;whiteSpace=wrap;html=1`
- Decision: `rhombus;whiteSpace=wrap;html=1`
- Database: `shape=cylinder3d;boundedLbl=1;backgroundOutline=1;size=15;whiteSpace=wrap;html=1`
- Circle/ellipse: `ellipse;whiteSpace=wrap;html=1`
- Plain text: `text;html=1;strokeColor=none;fillColor=none`

Consult `style-reference.md` for additional draw.io style vocabulary.

## Common Failures

- Invented palette instead of sampled colors.
- Labels copied with missing punctuation or wrong line breaks.
- Text clipped because geometry is too small.
- Arrow endpoints not attached to source/target boundaries.
- Using one embedded image instead of editable cells.
- Over-correcting into a cleaner style that no longer matches the source.
- Forgetting `fontFamily=Arial`.
