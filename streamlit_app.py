import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from heizoel.render import load_data, render_dashboard

DEFAULT_DATA_PATH = Path(__file__).parent / "data" / "heizoel_data.json"

st.set_page_config(page_title="Heizöl-Kaufberater", page_icon="🛢️", layout="wide")

if "raw_json" not in st.session_state:
    st.session_state.raw_json = DEFAULT_DATA_PATH.read_text(encoding="utf-8")

with st.sidebar:
    st.header("Daten")
    st.caption(
        "Diese App zeigt nur an. Die Werte kommen aus einer JSON-Datei, "
        "die du bei jedem Update selbst ersetzt (z. B. aus deinem "
        "bestehenden Recherche-Workflow für den Heizöl-Kaufberater)."
    )
    uploaded = st.file_uploader("Neue Datenversion hochladen (.json)", type="json")
    if uploaded is not None:
        st.session_state.raw_json = uploaded.read().decode("utf-8")

    if st.button("Auf Beispieldaten zurücksetzen"):
        st.session_state.raw_json = DEFAULT_DATA_PATH.read_text(encoding="utf-8")
        st.rerun()

    with st.expander("JSON direkt bearbeiten"):
        st.session_state.raw_json = st.text_area(
            "Daten", value=st.session_state.raw_json, height=400, label_visibility="collapsed"
        )

    st.download_button(
        "Aktuelle Daten als JSON speichern",
        data=st.session_state.raw_json,
        file_name="heizoel_data.json",
        mime="application/json",
    )

try:
    data = json.loads(st.session_state.raw_json)
except json.JSONDecodeError as e:
    st.error(f"Die JSON-Daten sind ungültig: {e}")
    st.stop()

try:
    html = render_dashboard(data)
except KeyError as e:
    st.error(f"In den Daten fehlt ein Feld, das die Vorlage erwartet: {e}")
    st.stop()

components.html(html, height=3400, scrolling=True)
