import streamlit as st
from utils.seats import calculate_seats
from utils.data_loader import get_first_votes
from utils.utils import get_winner_party
import pandas as pd
import plotly.express as px
from components.map import party_to_color

def create_direct_vs_total():
    """Create comparison of direct mandates vs total seats"""
    
    # Get seats and direct winners
    seats = calculate_seats()
    votes = get_first_votes()
    
    # Calculate direct winners
    direct_winners = get_winner_party(votes)
    direct_winners = direct_winners.value_counts().to_frame().reset_index().rename(
        columns={'index': 'Gruppenname', 'count': 'Sitze'}
    )
    
    # Combine CDU and CSU in direct winners
    cdu_csu_mask = direct_winners['Gruppenname'].isin(['CDU', 'CSU'])
    cdu_csu_seats = direct_winners[cdu_csu_mask]['Sitze'].sum()
    direct_winners = direct_winners[~cdu_csu_mask]
    direct_winners = pd.concat([
        direct_winners,
        pd.DataFrame([{
            'Gruppenname': 'CDU/CSU',
            'Sitze': cdu_csu_seats
        }])
    ])
    
    # Prepare data for plotting
    direct_winners['type'] = 'Direktmandate'
    seats['type'] = 'Gesamtsitze'
    plot_data = pd.concat([direct_winners, seats])
    
    # Update color map for combined parties
    color_map = party_to_color.copy()
    color_map['CDU/CSU'] = party_to_color['CDU']
    
    # Create bar plot
    fig = px.bar(
        plot_data,
        x='type',
        y='Sitze',
        color='Gruppenname',
        barmode='group',
        color_discrete_map=color_map,
        title='Direktmandate vs. Gesamtsitze'
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title='Mandat',
        yaxis_title='Anzahl Sitze',
        showlegend=True,
        xaxis_tickangle=0,
        legend_title='Partei'
    )
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True)



