import streamlit as st
from utils.data_loader import get_first_votes
import plotly.express as px
from components.map import party_to_color

def display_wahlkreis_info(df_map, selected_points):
    """Display information for selected Wahlkreis"""
    if not selected_points:
        st.title("Wahlkreisergebnisse")
        st.write("Klicken Sie auf einen Wahlkreis in der Karte, um detaillierte Ergebnisse anzuzeigen.")
        return
        
    
    # Get the WKR_NR from the customdata
    curve_number = selected_points[0]['curveNumber']
    point_number = selected_points[0]['pointNumber']
    
    # Find the corresponding row in df_map
    unique_winners = df_map['winner'].unique()
    winner_color = unique_winners[curve_number]
    selected_row = df_map[df_map['winner'] == winner_color].iloc[point_number]
    
    selected_wkr_nr = selected_row['WKR_NR']
    selected_wkr_name = selected_row['WKR_NAME']
    
    st.session_state.selected_wahlkreis = selected_wkr_nr
    
    st.subheader(f"Wahlkreis {selected_wkr_nr}: {selected_wkr_name}")
    st.write(f"Gewinner: {winner_color}")

    votes = get_first_votes()
    # filter by wkr_nr and sort by votes
    wkr_votes = votes[votes['Gebietsnummer'] == selected_wkr_nr].sort_values('Anzahl', ascending=False)
    if wkr_votes.empty or wkr_votes['Anzahl'].sum() == 0:
        st.info("Die Stimmen werden noch ausgezählt. Die Ergebnisse werden angezeigt, sobald sie vom Bundeswahlleiter freigegeben wurden.")
        return
    # Get top 8 parties by votes
    top_8_votes = wkr_votes.head(8)
    
    # Calculate percentages
    total_votes = wkr_votes['Anzahl'].sum()
    top_8_votes['Prozent'] = top_8_votes['Anzahl'] / total_votes * 100
    # Format percentage with 1 decimal place
    top_8_votes['Prozent_fmt'] = top_8_votes['Prozent'].apply(lambda x: f'{x:.1f}%')

    # Add toggle for absolute/percentage view
    show_percentage = st.toggle('Prozentuale Ansicht', value=False)

    # Prepare the figure based on toggle selection
    if show_percentage:
        y_col = 'Prozent'
        y_title = 'Prozent'
        y_values = top_8_votes['Prozent']
        text_values = top_8_votes['Prozent_fmt']
    else:
        y_col = 'Anzahl'
        y_title = 'Anzahl Stimmen'
        y_values = top_8_votes['Anzahl']
        # Format absolute numbers with thousands separator
        text_values = top_8_votes['Anzahl'].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))

    # Create figure
    fig = px.bar(
        top_8_votes,
        x='Gruppenname',
        y=y_col,
        color='Gruppenname',
        color_discrete_map=party_to_color,
        title='Erststimmen nach Partei (Top 8)',
        text=text_values
    )

    # Customize layout
    y_lim_multiplier = 1.2
    fig.update_layout(
        xaxis_title='Partei',
        yaxis_title=y_title,
        yaxis=dict(
            range=[0, max(y_values) * y_lim_multiplier]
        ),
        showlegend=False,
        xaxis_tickangle=45
    )

    # Position the text above bars
    fig.update_traces(textposition='outside', selector=dict(type='bar'))

    st.plotly_chart(fig)
