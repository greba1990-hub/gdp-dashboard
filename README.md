# 🛢️ Heizöl-Kaufberater

Streamlit-App, die das Heizöl-Kaufberater-Dashboard (Ampel, Preisband,
Tankfüllstand, Füllstandsprognose, Marktdaten, Lieferhistorie, Radar,
Kauflimit) im Originaldesign anzeigt.

Die App **berechnet oder recherchiert nichts selbst** – sie stellt nur dar,
was in `data/heizoel_data.json` steht. Diese Datei ersetzt du bei jedem
Update (z. B. aus deinem bestehenden Recherche-Workflow) über die Sidebar
(Upload, direkte JSON-Bearbeitung oder Zurücksetzen auf die Beispieldaten).

### Lokal ausführen

```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Aufbau

- `data/heizoel_data.json` – aktuelle Werte (Beispieldaten aus dem Stand
  10.09.2026)
- `templates/dashboard.html.j2` – Layout/CSS im Originaldesign
- `heizoel/charts.py` – berechnet die drei SVG-Grafiken (Preisband, Tank,
  Füllstandsprognose) aus den Rohwerten
- `heizoel/render.py` – lädt die Daten und rendert das Template
- `streamlit_app.py` – Sidebar zum Bearbeiten/Hochladen der Daten +
  Anzeige

### Datenstruktur ändern

Alle Felder in `data/heizoel_data.json` sind selbsterklärend benannt
(`ampel`, `kacheln`, `preisband`, `markt`, `tank`, `prognose`, `termine`,
`lieferhistorie`, `radar`, `limit`, `fuss`). Felder mit `_html` im Namen
dürfen einfaches HTML enthalten (`<b>`, `<b class="tw">` für Rot,
`<b class="tg">` für Grün), alle anderen Felder werden als reiner Text
angezeigt.
