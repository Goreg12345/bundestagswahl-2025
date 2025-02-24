import streamlit as st

def show_imprint():
    st.markdown("""
    # Impressum

    ## Angaben gemäß § 5 TMG
    Georg Lange

    ## Kontakt
    Bei Fragen oder Anregungen nutzen Sie bitte:
    [GitHub Issues](https://github.com/Goreg12345/bundestagswahl-2025/issues)

    ## Quellenangaben
    - Wahldaten: © Die Bundeswahlleiterin, Statistisches Bundesamt, 65180 Wiesbaden
    - Kartendaten: © Carto
    """)

def show_privacy():
    st.markdown("""
    # Datenschutzerklärung

    Stand: Februar 2025

    ## 1. Allgemeine Informationen
    Dies ist ein persönliches, nicht-kommerzielles Projekt zur Visualisierung öffentlich zugänglicher Wahldaten.

    ### Verantwortlicher im Sinne der DSGVO
    Georg Lange
    Kontakt über: [GitHub Issues](https://github.com/Goreg12345/bundestagswahl-2025/issues)

    ## 2. Datenverarbeitung
    - Diese Anwendung selbst speichert keine personenbezogenen Daten
    - Es werden keine Cookies durch die Anwendung gesetzt
    - Es werden keine Analyse-Tools verwendet

    ### Hosting und externe Dienste
    - Die Anwendung wird auf Streamlit Cloud gehostet. Die Datenschutzerklärung von Streamlit finden Sie [hier](https://streamlit.io/privacy-policy)
    - Für die Kartendarstellung nutzen wir Carto über Plotly. Die Datenschutzerklärung von Carto finden Sie [hier](https://carto.com/privacy)

    ## 3. Ihre Rechte
    Sie haben das Recht auf Auskunft, Berichtigung oder Löschung Ihrer Daten. Bei Fragen zum Datenschutz können Sie sich an die Thüringer Landesbeauftragte für den Datenschutz und die Informationsfreiheit wenden.

    ## 4. Datenquellen
    - Wahlergebnisse: © Die Bundeswahlleiterin, Statistisches Bundesamt, 65180 Wiesbaden
    - Kartendaten: © Carto
    """) 