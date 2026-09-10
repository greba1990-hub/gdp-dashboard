"""Lädt die Heizöl-Kaufberater-Daten und rendert sie ins Original-Layout."""

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from heizoel.charts import forecast_svg, percentile_band_svg, tank_svg

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"


def load_data(path: Path | str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def render_dashboard(data: dict) -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)
    template = env.get_template("dashboard.html.j2")
    return template.render(
        d=data,
        preisband_svg=percentile_band_svg(data["preisband"]),
        tank_svg=tank_svg(data["tank"]),
        prognose_svg=forecast_svg(data["prognose"]),
    )
