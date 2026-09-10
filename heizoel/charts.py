"""SVG-Generatoren für den Heizöl-Kaufberater.

Übersetzt die Zahlenwerte aus der Datendatei in dieselben SVG-Grafiken,
die im ursprünglichen Dashboard von Hand mit fixen Pixelkoordinaten
gebaut waren (Preisband, Tank, Füllstandsprognose).
"""

from html import escape


def _fmt(v, decimals=2):
    s = f"{v:,.{decimals}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def percentile_band_svg(band: dict) -> str:
    band_min = band["band_min"]
    band_max = band["band_max"]
    p10, p25 = band["p10"], band["p25"]
    heute, limit = band["heute"], band["limit"]

    x0, x1 = 30, 730
    span = max(band_max - band_min, 0.01)

    def x_of(v):
        return x0 + max(0.0, min(1.0, (v - band_min) / span)) * (x1 - x0)

    kaufzone_w = x_of(p25) - x0
    limit_x = x_of(p25)
    heute_x = x1 if heute >= band_max else x_of(heute)

    return f"""
  <svg viewBox="0 0 760 132" role="img" aria-label="Perzentilband mit Marker">
    <defs>
      <linearGradient id="bandg" x1="0" x2="1">
        <stop offset="0" stop-color="#14532d"/><stop offset="0.35" stop-color="#3f3f14"/>
        <stop offset="1" stop-color="#4c1416"/>
      </linearGradient>
    </defs>
    <rect x="{x0}" y="46" width="{x1 - x0}" height="24" rx="7" fill="url(#bandg)" stroke="#2c3644"/>
    <rect x="{x0}" y="46" width="{kaufzone_w:.1f}" height="24" rx="7" fill="#22c55e" opacity="0.42"/>
    <text x="{x0}" y="40" fill="#22c55e" font-size="11" font-family="sans-serif">Kaufzone ≤ {_fmt(p25)} €</text>
    <line x1="{limit_x:.1f}" y1="38" x2="{limit_x:.1f}" y2="78" stroke="#22c55e" stroke-width="2" stroke-dasharray="4 3"/>
    <text x="{limit_x + 4:.1f}" y="90" fill="#22c55e" font-size="11" font-family="sans-serif">Limit {_fmt(p25)}</text>
    <g>
      <line x1="{heute_x:.1f}" y1="34" x2="{heute_x:.1f}" y2="82" stroke="#ef4444" stroke-width="3"/>
      <circle cx="{heute_x:.1f}" cy="58" r="6" fill="#ef4444"/>
      <text x="{heute_x - 4:.1f}" y="28" fill="#ef4444" font-size="12" font-weight="700" text-anchor="end"
        font-family="sans-serif">HEUTE {_fmt(heute)} €</text>
    </g>
    <text x="{x0}" y="92" fill="#6b7a8c" font-size="11" font-family="sans-serif">{_fmt(band_min)} €</text>
    <text x="{x1}" y="92" fill="#6b7a8c" font-size="11" text-anchor="end"
      font-family="sans-serif">{_fmt(band_max)} €</text>
    <text x="{x0}" y="112" fill="#9aa8b8" font-size="11" font-family="sans-serif">
      P10 {_fmt(p10)} €  ·  P25 {_fmt(p25)} €  ·  Median {_fmt(band['median'])} €  ·  P75 {_fmt(band['p75'])} €</text>
    <text x="{x0}" y="128" fill="#6b7a8c" font-size="11" font-family="sans-serif">{escape(band.get('bandhinweis', ''))}</text>
  </svg>"""


def tank_svg(tank: dict) -> str:
    kap = tank["kapazitaet"]
    fuellstand = tank["fuellstand"]
    unschaerfe = tank.get("unschaerfe", 0)
    schwelle_rot = tank["schwelle_rot"]
    schwelle_orange = tank["schwelle_orange"]

    x0, y_bottom, y_top, height = 110, 330, 30, 300

    def y_of(v):
        return y_bottom - max(0.0, min(1.0, v / kap)) * height

    liquid_top = y_of(fuellstand)
    liquid_h = y_bottom - liquid_top
    unsch_top = y_of(fuellstand + unschaerfe)
    unsch_h = y_of(fuellstand - unschaerfe) - unsch_top

    return f"""
  <svg viewBox="0 0 800 410" role="img" aria-label="Tankfüllstand, liegender Zylindertank, Flüssigkeit steigt von unten">
    <defs>
      <clipPath id="tankClip">
        <rect x="110" y="30" width="580" height="300" rx="150" ry="150"/>
      </clipPath>
      <linearGradient id="tankShell" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#2c3644"/><stop offset="0.5" stop-color="#1c2430"/>
        <stop offset="1" stop-color="#141a22"/>
      </linearGradient>
      <linearGradient id="liquid" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#6ba6f8"/><stop offset="0.12" stop-color="#3b82f6"/>
        <stop offset="1" stop-color="#1d4ed8"/>
      </linearGradient>
      <pattern id="hatch" width="10" height="10" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
        <rect width="10" height="10" fill="none"/>
        <line x1="0" y1="0" x2="0" y2="10" stroke="#dce8f6" stroke-width="1.5" opacity="0.4"/>
      </pattern>
    </defs>
    <rect x="110" y="30" width="580" height="300" rx="150" ry="150" fill="url(#tankShell)"/>
    <g clip-path="url(#tankClip)">
      <rect x="110" y="{liquid_top:.2f}" width="580" height="{liquid_h:.2f}" fill="url(#liquid)"/>
      <rect x="110" y="{liquid_top:.2f}" width="580" height="4" fill="#bcd7fd" opacity="0.65"/>
      <rect x="110" y="{unsch_top:.2f}" width="580" height="{unsch_h:.2f}" fill="url(#hatch)"/>
      <rect x="110" y="30" width="580" height="52" fill="#ffffff" opacity="0.05"/>
    </g>
    <rect x="110" y="30" width="580" height="300" rx="150" ry="150" fill="none" stroke="#2c3644" stroke-width="2"/>
    <rect x="220" y="328" width="16" height="26" rx="2" fill="#1c2430" stroke="#2c3644"/>
    <rect x="564" y="328" width="16" height="26" rx="2" fill="#1c2430" stroke="#2c3644"/>
    <line x1="90" y1="356" x2="710" y2="356" stroke="#2c3644" stroke-width="2"/>
    <line x1="110" y1="{y_of(schwelle_rot):.2f}" x2="690" y2="{y_of(schwelle_rot):.2f}" stroke="#ef4444" stroke-width="1.8" stroke-dasharray="6 4"/>
    <line x1="110" y1="{y_of(schwelle_orange):.2f}" x2="690" y2="{y_of(schwelle_orange):.2f}" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="6 4"/>
    <text x="696" y="{y_of(schwelle_rot) + 5:.2f}" fill="#ef4444" font-size="13" font-family="sans-serif">{_fmt(schwelle_rot, 0)} l</text>
    <text x="696" y="{y_of(schwelle_orange) + 5:.2f}" fill="#f59e0b" font-size="13" font-family="sans-serif">{_fmt(schwelle_orange, 0)} l</text>
    <line x1="56" y1="{liquid_top:.2f}" x2="110" y2="{liquid_top:.2f}" stroke="#bcd7fd" stroke-width="1.5"/>
    <text x="52" y="{liquid_top - 4.4:.2f}" fill="#e8eef6" font-size="15" font-weight="700" text-anchor="end"
      font-family="sans-serif">≈ {_fmt(fuellstand, 0)} l</text>
    <text x="110" y="378" fill="#6b7a8c" font-size="12" font-family="sans-serif">0 l</text>
    <text x="690" y="378" fill="#6b7a8c" font-size="12" text-anchor="end" font-family="sans-serif">{_fmt(kap, 0)} l voll</text>
    <text x="400" y="398" fill="#9aa8b8" font-size="12" text-anchor="middle" font-family="sans-serif">
      Flüssigkeit steigt von unten · schraffiert = Modellunschärfe ± {_fmt(unschaerfe, 0)} l</text>
  </svg>"""


def forecast_svg(prognose: dict) -> str:
    monate = prognose["monate"]
    n = len(monate)
    y_max = prognose["y_max"]
    schwelle_rot = prognose["schwelle_rot"]
    schwelle_orange = prognose["schwelle_orange"]

    x0, x1, y0, y1 = 56, 740, 210, 24
    dx = (x1 - x0) / (n - 1)

    def x_of(i):
        return x0 + i * dx

    def y_of(v):
        return y0 - max(0.0, min(1.0, v / y_max)) * (y0 - y1)

    def yline(v, dash="5 4", color="#ef4444"):
        y = y_of(v)
        return f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{color}" stroke-width="1.5" stroke-dasharray="{dash}"/>'

    month_labels = "".join(
        f'<text x="{x_of(i):.1f}" y="243">{escape(m["label"])}</text>' for i, m in enumerate(monate)
    )

    sperr_rects = ""
    for lo, hi in prognose.get("sperrmonate_index", []):
        xa, xb = x_of(lo) - dx / 2, x_of(hi) + dx / 2
        sperr_rects += f'<rect x="{xa:.1f}" y="24" width="{xb - xa:.1f}" height="186" fill="url(#sperre)" opacity="0.85"/>'

    lief = prognose.get("lieferfenster_index")
    lief_rect = ""
    if lief:
        xa, xb = x_of(lief[0]) - dx / 2, x_of(lief[1]) + dx / 2
        lief_rect = f'<rect x="{xa:.1f}" y="24" width="{xb - xa:.1f}" height="186" fill="#22c55e" opacity="0.13"/>'

    high_pts = [(x_of(i), y_of(m["hoch"])) for i, m in enumerate(monate)]
    low_pts = [(x_of(i), y_of(m["tief"])) for i, m in enumerate(monate)]
    path_top = " ".join(f"L{x:.1f},{y:.1f}" for x, y in high_pts[1:])
    path_bottom = " ".join(f"L{x:.1f},{y:.1f}" for x, y in reversed(low_pts))
    band_path = (
        f"M{high_pts[0][0]:.1f},{high_pts[0][1]:.1f} {path_top} "
        f"L{x1},210 L{x0},210 {path_bottom} Z"
    )

    mid_pts = " ".join(f"{x_of(i):.1f},{y_of(m['mittel']):.1f}" for i, m in enumerate(monate))

    bestell = prognose.get("bestellmarke_index")
    bestell_marker = ""
    if bestell is not None:
        bx = x_of(bestell)
        by = y_of(monate[bestell]["mittel"])
        bestell_marker = f"""
    <line x1="{bx:.1f}" y1="18" x2="{bx:.1f}" y2="215" stroke="#a78bfa" stroke-width="2.5"/>
    <circle cx="{bx:.1f}" cy="{by:.1f}" r="5" fill="#a78bfa"/>
    <text x="{bx + 4:.1f}" y="16" fill="#a78bfa" font-size="11" font-weight="700"
      font-family="sans-serif">{escape(prognose.get('bestellmarke_label', ''))}</text>"""

    return f"""
  <svg viewBox="0 0 760 250" role="img" aria-label="Füllstandsprognose">
    <defs>
      <pattern id="sperre" width="7" height="7" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
        <rect width="7" height="7" fill="#0d1117"/>
        <line x1="0" y1="0" x2="0" y2="7" stroke="#7f5539" stroke-width="2.5"/>
      </pattern>
    </defs>
    {sperr_rects}
    {lief_rect}
    <g stroke="#202836"><line x1="{x0}" y1="210" x2="{x1}" y2="210"/>
      <line x1="{x0}" y1="{y_of(schwelle_rot):.1f}" x2="{x1}" y2="{y_of(schwelle_rot):.1f}"/>
      <line x1="{x0}" y1="{y_of(schwelle_orange):.1f}" x2="{x1}" y2="{y_of(schwelle_orange):.1f}"/>
      <line x1="{x0}" y1="24" x2="{x1}" y2="24"/></g>
    {yline(schwelle_rot, color="#ef4444")}
    {yline(schwelle_orange, color="#f59e0b")}
    <text x="60" y="{y_of(schwelle_rot) - 4:.1f}" fill="#ef4444" font-size="10" font-family="sans-serif">{_fmt(schwelle_rot, 0)} l Reserve</text>
    <text x="60" y="{y_of(schwelle_orange) - 4:.1f}" fill="#f59e0b" font-size="10" font-family="sans-serif">{_fmt(schwelle_orange, 0)} l bestellen</text>
    <path fill="#3b82f6" opacity="0.20" d="{band_path}"/>
    <polyline fill="none" stroke="#3b82f6" stroke-width="2.5" stroke-linejoin="round" points="{mid_pts}"/>
    {bestell_marker}
    <g fill="#6b7a8c" font-size="10" font-family="sans-serif" text-anchor="middle">{month_labels}</g>
    <g fill="#6b7a8c" font-size="10" font-family="sans-serif" text-anchor="end">
      <text x="50" y="28">{_fmt(y_max, 0)} l</text><text x="50" y="214">0 l</text>
    </g>
  </svg>"""
