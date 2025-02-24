import plotly.express as px
from utils.data_loader import get_first_votes
from utils.utils import get_winner_party, party_to_color


def create_wahlkreis_map(df, geojson_data):
    votes = get_first_votes()
    winners = get_winner_party(votes)
    
    # Create a copy and sort by WKR_NR to ensure consistent ordering
    df_map = df.copy().sort_values('WKR_NR')
    df_map['winner'] = df_map['WKR_NR'].map(winners)
    
    # Create hover text
    df_map['hover_text'] = df_map.apply(
        lambda x: f"{x['WKR_NAME']}<br>WKR {x['WKR_NR']}<br>{x['winner']}", 
        axis=1
    )
    
    fig = px.choropleth_mapbox(
        data_frame=df_map,
        geojson=geojson_data,
        locations='WKR_NR',
        featureidkey="properties.WKR_NR",
        color='winner',
        color_discrete_map=party_to_color,
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 51.1657, "lon": 10.4515},
        opacity=0.7,
        hover_name='hover_text'  # Use our custom hover text
    )

    # Simplify hover template
    fig.update_traces(
        hovertemplate="%{hovertext}<extra></extra>",
        marker_line_width=1,
        marker_line_color='white'
    )

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        height=800,
        showlegend=False
    )
    
    return fig, df_map 