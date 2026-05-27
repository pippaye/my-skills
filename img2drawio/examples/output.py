#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


WORKDIR = Path(__file__).resolve().parent


# CSS-like knobs only. Diagram structure, labels, geometry, and connections
# live in DRAWIO_TEMPLATE below.
CONFIG = {
    "font_family": "Arial",
    "page_bg": "#FFFFFF",
    "border": "#1F365C",
    "gpu_fill": "#BDD7ED",
    "channel_fill": "#FFE699",
    "nic_fill": "#C6E0B4",
    "cpu_fill": "#F8CBAD",
    "region_fill": "#F5F5F5",
    "red": "#C00000",
    "black": "#000000",
    "stroke_width": 2,
    "arrow_width": 3,
    "label_font": 28,
    "small_font": 22,
    "title_font": 28,
    "role_font": 30,
}


def style(**items: object) -> str:
    merged = {"fontFamily": CONFIG["font_family"]}
    merged.update(items)
    return ";".join(f"{key}={value}" for key, value in merged.items() if value is not None) + ";"


STYLES = {
    "region": style(
        rounded=0,
        whiteSpace="wrap",
        html=1,
        fillColor=CONFIG["region_fill"],
        strokeColor=CONFIG["border"],
        strokeWidth=CONFIG["stroke_width"],
        fontSize=CONFIG["label_font"],
    ),
    "gpu_buffer": style(
        rounded=0,
        whiteSpace="wrap",
        html=1,
        fillColor=CONFIG["gpu_fill"],
        strokeColor=CONFIG["border"],
        strokeWidth=CONFIG["stroke_width"],
        fontSize=CONFIG["label_font"],
    ),
    "channel": style(
        rounded=0,
        whiteSpace="wrap",
        html=1,
        fillColor=CONFIG["channel_fill"],
        strokeColor=CONFIG["border"],
        strokeWidth=CONFIG["stroke_width"],
        fontSize=CONFIG["label_font"],
    ),
    "nic": style(
        rounded=0,
        whiteSpace="wrap",
        html=1,
        fillColor=CONFIG["nic_fill"],
        strokeColor=CONFIG["border"],
        strokeWidth=CONFIG["stroke_width"],
        fontSize=CONFIG["label_font"],
    ),
    "cpu": style(
        rounded=0,
        whiteSpace="wrap",
        html=1,
        fillColor=CONFIG["cpu_fill"],
        strokeColor=CONFIG["border"],
        strokeWidth=CONFIG["stroke_width"],
        fontSize=CONFIG["title_font"],
    ),
    "text": style(
        text=1,
        html=1,
        strokeColor="none",
        fillColor="none",
        fontSize=CONFIG["label_font"],
        align="center",
        verticalAlign="middle",
    ),
    "red_role": style(
        text=1,
        html=1,
        strokeColor="none",
        fillColor="none",
        fontColor=CONFIG["red"],
        fontStyle=1,
        fontSize=CONFIG["role_font"],
        align="center",
        verticalAlign="middle",
    ),
    "edge": style(
        endArrow="classic",
        html=1,
        rounded=0,
        edgeStyle="orthogonalEdgeStyle",
        strokeColor=CONFIG["black"],
        strokeWidth=CONFIG["arrow_width"],
    ),
    "line": style(
        shape="line",
        strokeColor=CONFIG["black"],
        strokeWidth=CONFIG["arrow_width"],
    ),
    "curve": style(
        endArrow="classic",
        html=1,
        curved=1,
        rounded=0,
        strokeColor=CONFIG["black"],
        strokeWidth=CONFIG["arrow_width"],
    ),
}


DRAWIO_TEMPLATE = """<mxfile host="app.diagrams.net" modified="2026-05-27T00:00:00.000Z" agent="img2drawio" version="28.0.0">
  <diagram id="rdma-flow" name="RDMA Flow">
    <mxGraphModel dx="1534" dy="626" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1534" pageHeight="626" background="{page_bg}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <mxCell id="sender_label" value="SENDER" style="{red_role}" vertex="1" parent="1">
          <mxGeometry x="50" y="65" width="150" height="45" as="geometry"/>
        </mxCell>
        <mxCell id="receiver_label" value="RECEIVER" style="{red_role}" vertex="1" parent="1">
          <mxGeometry x="1330" y="65" width="165" height="45" as="geometry"/>
        </mxCell>

        <mxCell id="sender_hbm" value="GPU HBM" style="{region}verticalAlign=bottom;spacingBottom=12;fontSize=30;" vertex="1" parent="1">
          <mxGeometry x="36" y="176" width="448" height="366" as="geometry"/>
        </mxCell>
        <mxCell id="receiver_hbm" value="GPU HBM" style="{region}verticalAlign=bottom;spacingBottom=12;fontSize=30;" vertex="1" parent="1">
          <mxGeometry x="1049" y="177" width="441" height="367" as="geometry"/>
        </mxCell>

        <mxCell id="sender_compute" value="Compute&lt;br&gt;Buffer" style="{gpu_buffer}" vertex="1" parent="1">
          <mxGeometry x="55" y="196" width="180" height="280" as="geometry"/>
        </mxCell>
        <mxCell id="receiver_compute" value="Compute&lt;br&gt;Buffer" style="{gpu_buffer}" vertex="1" parent="1">
          <mxGeometry x="1294" y="202" width="181" height="276" as="geometry"/>
        </mxCell>

        <mxCell id="sender_channel_1" value="Channel&lt;br&gt;Buffer" style="{channel}" vertex="1" parent="1">
          <mxGeometry x="304" y="202" width="165" height="91" as="geometry"/>
        </mxCell>
        <mxCell id="sender_channel_2" value="Channel&lt;br&gt;Buffer" style="{channel}" vertex="1" parent="1">
          <mxGeometry x="302" y="311" width="164" height="90" as="geometry"/>
        </mxCell>
        <mxCell id="receiver_channel_1" value="Channel&lt;br&gt;Buffer" style="{channel}" vertex="1" parent="1">
          <mxGeometry x="1059" y="200" width="164" height="90" as="geometry"/>
        </mxCell>
        <mxCell id="receiver_channel_2" value="Channel&lt;br&gt;Buffer" style="{channel}" vertex="1" parent="1">
          <mxGeometry x="1057" y="309" width="165" height="89" as="geometry"/>
        </mxCell>

        <mxCell id="sender_cpu" value="CPU proxy" style="{cpu}" vertex="1" parent="1">
          <mxGeometry x="304" y="57" width="374" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="receiver_cpu" value="CPU proxy" style="{cpu}" vertex="1" parent="1">
          <mxGeometry x="858" y="58" width="374" height="60" as="geometry"/>
        </mxCell>

        <mxCell id="sender_nic" value="RDMA&lt;br&gt;NIC" style="{nic}" vertex="1" parent="1">
          <mxGeometry x="548" y="202" width="135" height="90" as="geometry"/>
        </mxCell>
        <mxCell id="receiver_nic" value="RDMA&lt;br&gt;NIC" style="{nic}" vertex="1" parent="1">
          <mxGeometry x="846" y="200" width="134" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="free_label" value="Free" style="{text}fontSize=28;" vertex="1" parent="1">
          <mxGeometry x="306" y="145" width="72" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="rdma_write_label" value="RDMA write" style="{text}fontSize=28;" vertex="1" parent="1">
          <mxGeometry x="448" y="145" width="165" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="cts_label" value="CTS" style="{text}fontSize=28;" vertex="1" parent="1">
          <mxGeometry x="821" y="146" width="62" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="complete_label" value="Complete" style="{text}fontSize=28;" vertex="1" parent="1">
          <mxGeometry x="927" y="146" width="130" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="flush_label" value="Flush" style="{text}fontSize=28;" vertex="1" parent="1">
          <mxGeometry x="1150" y="146" width="88" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="network_label" value="RDMA&lt;br&gt;network" style="{text}fontSize=32;" vertex="1" parent="1">
          <mxGeometry x="710" y="260" width="130" height="76" as="geometry"/>
        </mxCell>
        <mxCell id="copy_left" value="Copy" style="{text}fontSize=28;" vertex="1" parent="1">
          <mxGeometry x="236" y="203" width="70" height="35" as="geometry"/>
        </mxCell>
        <mxCell id="copy_right" value="Copy" style="{text}fontSize=28;" vertex="1" parent="1">
          <mxGeometry x="1228" y="198" width="70" height="35" as="geometry"/>
        </mxCell>
        <mxCell id="dma_left" value="DMA" style="{text}fontSize=28;" vertex="1" parent="1">
          <mxGeometry x="482" y="211" width="70" height="35" as="geometry"/>
        </mxCell>
        <mxCell id="dma_right" value="DMA" style="{text}fontSize=28;" vertex="1" parent="1">
          <mxGeometry x="986" y="210" width="70" height="35" as="geometry"/>
        </mxCell>
        <mxCell id="sender_dots" value="•  •  •" style="{text}fontSize=34;" vertex="1" parent="1">
          <mxGeometry x="340" y="430" width="100" height="35" as="geometry"/>
        </mxCell>
        <mxCell id="receiver_dots" value="•  •  •" style="{text}fontSize=34;" vertex="1" parent="1">
          <mxGeometry x="1094" y="426" width="100" height="35" as="geometry"/>
        </mxCell>

        <mxCell id="e_cpu_sender_channel" value="" style="{edge}exitX=0.22;exitY=1;entryX=0.5;entryY=0;" edge="1" parent="1" source="sender_cpu" target="sender_channel_1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e_cpu_receiver_channel" value="" style="{edge}exitX=0.75;exitY=1;entryX=0.5;entryY=0;" edge="1" parent="1" source="receiver_cpu" target="receiver_channel_1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e_sender_compute_channel" value="" style="{edge}exitX=1;exitY=0.18;entryX=0;entryY=0.5;" edge="1" parent="1" source="sender_compute" target="sender_channel_1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e_sender_compute_channel_2" value="" style="{edge}exitX=1;exitY=0.57;entryX=0;entryY=0.5;" edge="1" parent="1" source="sender_compute" target="sender_channel_2">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e_sender_compute_dots" value="" style="{edge}exitX=1;exitY=0.9;entryX=0;entryY=0.5;" edge="1" parent="1" source="sender_compute" target="sender_dots">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e_sender_channel_nic" value="" style="{edge}exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="sender_channel_1" target="sender_nic">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e_sender_nic_receiver_nic" value="" style="{edge}exitX=1;exitY=0.48;entryX=0;entryY=0.5;" edge="1" parent="1" source="sender_nic" target="receiver_nic">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e_receiver_nic_channel" value="" style="{edge}exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="receiver_nic" target="receiver_channel_1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e_receiver_channel_compute" value="" style="{edge}exitX=1;exitY=0.5;entryX=0;entryY=0.15;" edge="1" parent="1" source="receiver_channel_1" target="receiver_compute">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e_receiver_channel_compute_2" value="" style="{edge}exitX=1;exitY=0.5;entryX=0;entryY=0.54;" edge="1" parent="1" source="receiver_channel_2" target="receiver_compute">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e_receiver_dots_compute" value="" style="{edge}exitX=1;exitY=0.5;entryX=0;entryY=0.88;" edge="1" parent="1" source="receiver_dots" target="receiver_compute">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e_sender_nic_cpu" value="" style="{edge}exitX=0.5;exitY=0;entryX=0.87;entryY=1;" edge="1" parent="1" source="sender_nic" target="sender_cpu">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e_receiver_nic_cpu" value="" style="{edge}exitX=0.5;exitY=0;entryX=0.15;entryY=1;" edge="1" parent="1" source="receiver_nic" target="receiver_cpu">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e_cts_curve" value="" style="{curve}" edge="1" parent="1" source="sender_nic" target="receiver_nic">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="635" y="228"/>
              <mxPoint x="750" y="245"/>
              <mxPoint x="895" y="120"/>
            </Array>
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""


def main() -> None:
    output = DRAWIO_TEMPLATE.format(page_bg=CONFIG["page_bg"], **STYLES)
    (WORKDIR / "output.drawio").write_text(output, encoding="utf-8")
    print(WORKDIR / "output.drawio")


if __name__ == "__main__":
    main()
