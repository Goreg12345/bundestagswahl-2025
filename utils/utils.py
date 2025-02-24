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