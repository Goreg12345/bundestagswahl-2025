# Here, we will calculate the seats for each party based on the votes and the seats in the Bundestag

# This is based on the Bundeswahlgesetz (BWG)

import pandas as pd
from utils.data_loader import get_second_votes, get_first_votes

def combine_cdu_csu(total_by_party):
    cdu_csu_mask = total_by_party['Gruppenname'].isin(['CDU', 'CSU'])
    cdu_csu_votes = total_by_party[cdu_csu_mask]['Anzahl'].sum()
    
    # Remove individual CDU and CSU rows and add combined row
    total_by_party = total_by_party[~cdu_csu_mask]
    total_by_party = pd.concat([
        total_by_party,
        pd.DataFrame([{
            'Gruppenname': 'CDU/CSU',
            'Anzahl': cdu_csu_votes
        }])
    ])
    return total_by_party

def calculate_winner(votes):
    # if they are empty, return empty string or nan
    sum_votes = votes.Anzahl.sum()
    if pd.isna(sum_votes) or sum_votes == 0:
        return ""
    return votes.loc[votes['Anzahl'].idxmax(), 'Gruppenname']

def n_independent_mandates():
    # these are the mandates that are not allocated by the party list
    votes = get_first_votes()

    district_winners = votes.groupby('Gebietsnummer').apply(calculate_winner)
    # now, count the number of independent mandates
    # count the number of "EB:*" in the district_winners
    independent_mandates = district_winners[district_winners.str.contains('EB:')].count()
    # count the SSW as a "Partei nationaler Minderheiten" 
    independent_mandates += district_winners[district_winners.str.contains('SSW')].count()
    return independent_mandates

    # independent mandates have the party name "EB:*"

def five_percent_rule(total_by_party):
    # Get first votes to check wahlkreis winners
    first_votes = get_first_votes()
    district_winners = first_votes.groupby('Gebietsnummer').apply(calculate_winner)
    
    # Count wahlkreis winners per party
    wahlkreis_winners = district_winners.value_counts()
    
    # Calculate total votes
    total_votes = total_by_party['Anzahl'].sum()
    
    # A party is exempt if they:
    # 1. Have > 5% of votes
    # 2. Are the SSW (party of national minorities)
    # 3. Have at least 3 wahlkreis winners
    five_percent_mask = (
        (total_by_party['Anzahl'] > 0.05 * total_votes) | 
        (total_by_party['Gruppenname'] == 'SSW') |
        (total_by_party['Gruppenname'].map(lambda x: wahlkreis_winners.get(x, 0) >= 3))
    )
    
    total_by_party = total_by_party[five_percent_mask]
    return total_by_party


def custom_round(x):
    i = int(x)
    f = x - i
    if f > 0.5:
        return i + 1
    if f < 0.5:
        return i
    return i  # Bei exakt 0.5 könnte man ein Losverfahren einbauen

def seats_for_divisor(votes, divisor):
    return [custom_round(v/divisor) for v in votes]

def allocate_seats(df, total_seats):
    votes = df['Anzahl'].tolist()
    low = 0.000001
    high = max(votes)
    for _ in range(200):
        mid = (low + high) / 2
        alloc = seats_for_divisor(votes, mid)
        s = sum(alloc)
        if s > total_seats:
            low = mid
        elif s < total_seats:
            high = mid
        else:
            break
    final_alloc = seats_for_divisor(votes, mid)
    return pd.DataFrame({
        'Gruppenname': df['Gruppenname'],
        'Sitze': final_alloc
    })


def calculate_seats() -> pd.DataFrame:
    """
    Calculate the seats for each party based on the votes and the seats in the Bundestag
    """
    votes = get_second_votes()
    # Calculate total votes and percentages for all of Germany
    total_by_party = votes.groupby('Gruppenname')['Anzahl'].sum().astype(int).reset_index()
    total_by_party = combine_cdu_csu(total_by_party)
    total_by_party = five_percent_rule(total_by_party)

    # $4.1 Von der Gesamtzahl der Sitze wird die Zahl der nach § 6
    # Absatz 2 erfolgreichen Wahlkreisbewerber abgezogen.    
    seats_in_bundestag = 630 - n_independent_mandates()

    # distribute the seats
    seats = allocate_seats(total_by_party, seats_in_bundestag)

    return seats

if __name__ == "__main__":
    seats = calculate_seats()
    print(seats)