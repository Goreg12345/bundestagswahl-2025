import streamlit as st
import plotly.express as px
from utils.data_loader import get_second_votes
from components.map import party_to_color
import pandas as pd
from utils.seats import calculate_seats
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def create_overview():
    """Create overview section with Zweitstimmen results"""
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Add title
        st.subheader("Zweitstimmen bundesweit")
        # Add toggle for percentage/absolute
        show_absolute = st.toggle('Absolute Zahlen anzeigen', value=False)
        
        # Get second votes data
        votes = get_second_votes()
        
        # Calculate total votes and percentages for all of Germany
        total_by_party = votes.groupby('Gruppenname')['Anzahl'].sum().reset_index()
        
        # Combine CDU and CSU
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
        
        # Calculate percentages
        total_votes = total_by_party['Anzahl'].sum()
        total_by_party['Prozent'] = total_by_party['Anzahl'] / total_votes * 100
        
        # Sort by percentage and split into top 7 and others
        total_by_party = total_by_party.sort_values('Prozent', ascending=False)
        top_7 = total_by_party.head(7)
        others = pd.DataFrame([{
            'Gruppenname': 'Sonstige',
            'Anzahl': total_by_party.iloc[7:]['Anzahl'].sum(),
            'Prozent': total_by_party.iloc[7:]['Prozent'].sum()
        }])
        
        # Combine top 7 and others
        plot_data = pd.concat([top_7, others])
        
        # Format numbers for display
        if show_absolute:
            y_col = 'Anzahl'
            y_title = 'Anzahl Stimmen'
            plot_data['display_value'] = plot_data['Anzahl'].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))
            hurdle_value = total_votes * 0.05  # 5% of total votes
        else:
            y_col = 'Prozent'
            y_title = 'Prozent'
            plot_data['display_value'] = plot_data['Prozent'].apply(
                lambda x: f'{x:.3f}%' if 4.9 <= x <= 5.1 else f'{x:.1f}%'
            )
            hurdle_value = 5.0
        
        # Update color map for combined parties
        color_map = party_to_color.copy()
        color_map['CDU/CSU'] = party_to_color['CDU']
        color_map['Sonstige'] = '#808080'  # Grey for others
        
        # Create bar plot
        fig = px.bar(
            plot_data,
            x='Gruppenname',
            y=y_col,
            color='Gruppenname',
            color_discrete_map=color_map,
            text='display_value'
        )
        
        # Add 5% hurdle line
        fig.add_hline(
            y=hurdle_value,
            line_dash="dash",
            line_color="grey",
            annotation_text="5% Hürde",
            annotation_position="right"
        )
        
        # Update layout
        fig.update_layout(
            #title='Zweitstimmen bundesweit',
            xaxis_title='Partei',
            yaxis_title=y_title,
            showlegend=False,
            xaxis_tickangle=45,
            yaxis=dict(
                range=[0, max(plot_data[y_col]) * 1.2]  # Add 20% space for labels
            )
        )
        
        # Position text above bars
        fig.update_traces(textposition='outside')
        
        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sitzverteilung im Bundestag")
        seats = calculate_seats()
        # Create bar plot for seats
        seats['color'] = seats['Gruppenname'].map(lambda x: color_map.get(x, '#808080'))
        # Create half-circle plot for parliament seats
        total_seats = seats['Sitze'].sum()
        
        # Add dummy row at the end for white background
        seats = pd.concat([
            seats,
            pd.DataFrame([{
                'Gruppenname': ' ',
                'Sitze': total_seats,
                'color': 'rgba(0, 0, 0, 0)'
            }])
        ])
        # Sort parties from left to right
        party_order = ['Die Linke', 'BSW', 'GRÜNE', 'SPD', 'SSW', 'CDU/CSU', 'FDP', 'AfD', ' ']
        seats = seats[seats['Gruppenname'].isin(party_order)].set_index('Gruppenname').reindex(party_order).reset_index()
        seats = seats.dropna()
        fig = go.Figure()

        fig.add_trace(go.Pie(
            values=seats['Sitze'],
            labels=seats['Gruppenname'],
            marker_colors=seats['color'],
            textinfo='value',
            textposition='outside',
            showlegend=True,
            hole=0.4,
            direction='clockwise',
            rotation=90,
           # domain=dict(x=[0, 1], y=[0, .8])  # Only show top half
        ))

        fig.update_layout(
            #margin=dict(t=80, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom", 
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            annotations=[
                dict(
                    text=f'Gesamt: {total_seats} Sitze',
                    x=0.5,
                    y=0.3,  # Adjusted y position for half circle
                    font_size=20,
                    showarrow=False
                )
            ]
        )

        st.plotly_chart(fig, use_container_width=True)


    return None  # Since we're displaying the plot directly in the function
