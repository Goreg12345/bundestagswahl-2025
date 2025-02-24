import geopandas as gpd
import pandas as pd
import json
import streamlit as st
import glob
import os


@st.cache_data
def load_geojson():
    """Load and process the shapefile data"""
    return gpd.read_file("shapefiles/btw25_geometrie_wahlkreise_shp_geo.shp").to_json()

def process_geojson(geojson_str):
    """Convert GeoJSON string to DataFrame with required columns"""
    geojson_data = json.loads(geojson_str)
    return pd.DataFrame([{
        'WKR_NR': f['properties']['WKR_NR'],
        'WKR_NAME': f['properties']['WKR_NAME']
    } for f in geojson_data['features']]) 

@st.cache_data
def load_election_results():
    """Load and process election results data"""

    kerg2_files = glob.glob('results/kerg2_*.csv')
    newest_file = max(kerg2_files, key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))
    
    # Load raw results, skipping header rows
    results = pd.read_csv(newest_file, delimiter=';', skiprows=9)
    
    # Filter for Wahlkreis level results
    results = results[results.Gebietsart == 'Wahlkreis']
    
    return results

@st.cache_data 
def get_first_votes():
    """Get first votes (Erststimmen) results by party"""
    results = load_election_results()
    return results[(results.Stimme == 1) & (results.Gruppenart=='Partei')]

@st.cache_data
def get_second_votes():
    """Get second votes (Zweitstimmen) results by party"""
    results = load_election_results()
    return results[(results.Stimme == 2) & (results.Gruppenart=='Partei')]