import streamlit as st
from streamlit_plotly_events import plotly_events
import json

from utils.data_loader import load_geojson, process_geojson
from components.map import create_wahlkreis_map
from components.results import display_wahlkreis_info
from components.legal import show_imprint, show_privacy
from components.overview import create_overview

# Page config
st.set_page_config(
    page_title="Bundestagswahl 2025",
    layout="wide",
    page_icon="🗳️"
)
st.title("Bundestagswahl 2025")

# Add overview section
create_overview()

# Add separator
st.markdown("---")

# Load and process data
geojson_str = load_geojson()
geojson_data = json.loads(geojson_str)
df = process_geojson(geojson_str)

# Initialize session state
if 'selected_wahlkreis' not in st.session_state:
    st.session_state.selected_wahlkreis = None

# Create layout for map and details
col1, col2 = st.columns(2)

# Create and display map
with col1:
    fig, df_map = create_wahlkreis_map(df, geojson_data)
    selected_points = plotly_events(fig, click_event=True, override_height=800)

# Display results
with col2:
    display_wahlkreis_info(df_map, selected_points)

# Footer with legal info
st.markdown("---")
if st.button("Impressum"):
    show_imprint()
if st.button("Datenschutzerklärung"):
    show_privacy()