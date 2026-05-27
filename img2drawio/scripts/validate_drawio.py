#!/usr/bin/env python3
"""Validate a .drawio file with XSD plus lightweight semantic checks."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from lxml import etree


def parse_xml(path: Path) -> etree._ElementTree:
    parser = etree.XMLParser(remove_blank_text=False, resolve_entities=False, no_network=True)
    return etree.parse(str(path), parser)


def validate_xsd(tree: etree._ElementTree, xsd_path: Path) -> list[str]:
    schema_doc = parse_xml(xsd_path)
    schema = etree.XMLSchema(schema_doc)
    if schema.validate(tree):
        return []
    return [str(error) for error in schema.error_log]


def semantic_errors(tree: etree._ElementTree) -> list[str]:
    errors: list[str] = []
    root = tree.getroot()

    if root.tag != "mxfile":
        errors.append("Root element must be <mxfile>.")

    diagrams = root.findall("diagram")
    if not diagrams:
        errors.append("No <diagram> element found.")
        return errors

    for diagram_index, diagram in enumerate(diagrams, start=1):
        graph_model = diagram.find("mxGraphModel")
        if graph_model is None:
            errors.append(f"Diagram {diagram_index}: missing <mxGraphModel>.")
            continue

        model_root = graph_model.find("root")
        if model_root is None:
            errors.append(f"Diagram {diagram_index}: missing <root> inside mxGraphModel.")
            continue

        cells = model_root.findall("mxCell")
        cells_by_id = {cell.get("id"): cell for cell in cells if cell.get("id")}

        if "0" not in cells_by_id:
            errors.append(f"Diagram {diagram_index}: missing mxCell id='0'.")
        if "1" not in cells_by_id:
            errors.append(f"Diagram {diagram_index}: missing default layer mxCell id='1'.")
        elif cells_by_id["1"].get("parent") != "0":
            errors.append(f"Diagram {diagram_index}: mxCell id='1' must have parent='0'.")

        for cell in cells:
            cell_id = cell.get("id", "<missing id>")
            parent = cell.get("parent")
            if parent and parent not in cells_by_id:
                errors.append(f"Diagram {diagram_index}: cell {cell_id} has missing parent {parent}.")

            if cell.get("edge") == "1":
                source = cell.get("source")
                target = cell.get("target")
                if not source:
                    errors.append(f"Diagram {diagram_index}: edge {cell_id} is missing source.")
                elif source not in cells_by_id:
                    errors.append(f"Diagram {diagram_index}: edge {cell_id} source {source} does not exist.")
                if not target:
                    errors.append(f"Diagram {diagram_index}: edge {cell_id} is missing target.")
                elif target not in cells_by_id:
                    errors.append(f"Diagram {diagram_index}: edge {cell_id} target {target} does not exist.")

                geometry = cell.find("mxGeometry")
                if geometry is None:
                    errors.append(f"Diagram {diagram_index}: edge {cell_id} missing mxGeometry.")
                elif geometry.get("relative") != "1":
                    errors.append(f"Diagram {diagram_index}: edge {cell_id} mxGeometry should use relative='1'.")

            if cell.get("vertex") == "1":
                geometry = cell.find("mxGeometry")
                if geometry is None:
                    errors.append(f"Diagram {diagram_index}: vertex {cell_id} missing mxGeometry.")
                else:
                    for attr in ("x", "y", "width", "height"):
                        if geometry.get(attr) is None:
                            errors.append(f"Diagram {diagram_index}: vertex {cell_id} geometry missing {attr}.")

            style = cell.get("style", "")
            has_text = bool(cell.get("value")) or style.startswith("text;") or "fontSize=" in style
            if has_text and "fontFamily=Arial" not in style:
                errors.append(f"Diagram {diagram_index}: text-bearing cell {cell_id} missing fontFamily=Arial.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a .drawio file.")
    parser.add_argument("drawio", type=Path)
    parser.add_argument("xsd", type=Path)
    args = parser.parse_args()

    if not args.drawio.exists():
        print(f"Draw.io file not found: {args.drawio}", file=sys.stderr)
        return 1
    if not args.xsd.exists():
        print(f"XSD file not found: {args.xsd}", file=sys.stderr)
        return 1

    try:
        tree = parse_xml(args.drawio)
    except etree.XMLSyntaxError as exc:
        print(f"XML syntax error: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    try:
        errors.extend(validate_xsd(tree, args.xsd))
    except etree.XMLSchemaParseError as exc:
        print(f"XSD parse error: {exc}", file=sys.stderr)
        return 1

    errors.extend(semantic_errors(tree))

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validation passed: {args.drawio}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
