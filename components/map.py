import plotly.express as px
from utils.data_loader import get_first_votes

party_to_color = {
    'CDU': '#000000',
    'SPD': '#E3000F',
    'GRÜNE': '#64A12D',
    'FDP': '#FFED00',
    'Die Linke': '#BE3075',
    'AfD': '#009FE3',
    'SSW': '#005392',
    'Die PARTEI': '#BE1E2D',
    'FREIE WÄHLER': '#FFA500',
    'Volt': '#5628AA',
    'MLPD': '#E00000',
    'BÜNDNIS DEUTSCHLAND': '#556B2F',
    'BSW': '#8B008B',
    'Tierschutzpartei': '#009E47',
    'dieBasis': '#DEB887',
    'PIRATEN': '#F7941D',
    'PdH': '#BDB76B',
    'Team Todenhöfer': '#483D8B',
    'ÖDP': '#F6801D',
    'MENSCHLICHE WELT': '#FF1493',
    'MERA25': '#00CED1',
    'Verjüngungsforschung': '#9400D3',
    'BüSo': '#FF8C00',
    'SGP': '#8FBC8F',
    'PdF': '#483D8B',
    'WerteUnion': '#8B0000',
    'Bündnis C': '#9932CC',
    'CSU': '#071630',
    'BP': '#8B008B',
    'EB': '#A9A9A9',
    'Keine Ergebnisse': '#808080'
}


def get_map_colors(df):
    def result_to_color(result):
        # are results already available?
        if result.Anzahl.sum() > 0:
            # Get the party with maximum votes
            max_party = result[result.Anzahl == result.Anzahl.max()].Gruppenname.iloc[0]
            
            # Handle Einzelbewerber (EB:*) cases
            if max_party.startswith('EB:'):
                return party_to_color['EB']
                
            # Return the color for the winning party
            return party_to_color[max_party]
        else:
            return '#808080'  # Return a grey color when no results available


    colors = df.groupby('Gebietsnummer').apply(result_to_color)
    return colors

def get_winner_party(df):
    def get_winner(result):
        # Check if results are available
        if result.Anzahl.sum() > 0:
            # Get the party with maximum votes
            max_party = result[result.Anzahl == result.Anzahl.max()].Gruppenname.iloc[0]
            
            # Handle Einzelbewerber (EB:*) cases
            if max_party.startswith('EB:'):
                return 'EB'
            return max_party
        else:
            return 'Keine Ergebnisse'  # Return message when no results available
            
    winners = df.groupby('Gebietsnummer').apply(get_winner)
    return winners


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