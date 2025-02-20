import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io
import math

# Dictionary of countries and leagues
leagues_dict = {
    "England": ["UK1", "UK2", "UK3", "UK4", "UK5", "UK6N", "UK6S", "UK7N"],
        "Germany": ["DE1", "DE2", "DE3", "DE4SW", "DE4W", "DE4N", "DE4NO", "DE4B"],
        "Italy": ["IT1", "IT2", "IT3C", "IT3B", "IT3A"],
        "Spain": ["ES1", "ES2", "ES3G1", "ES3G2", "ES3G3", "ES3G4", "ES3G5"],
        "France": ["FR1", "FR2", "FR3"],
        "Sweden": ["SW1", "SW2", "SW3S", "SW3N"],
        "Netherlands": ["NL1", "NL2", "NL3"],
        "Russia": ["RU1", "RU2"],
        "Portugal": ["PT1", "PT2"],
        "Austria": ["AT1", "AT2", "AT3O", "AT3T", "AT3M", "AT3W", "AT3V"],
        "Denmark": ["DK1", "DK2", "DK3G1", "DK3G2"],
        "Greece": ["GR1", "GR2"],
        "Norway": ["NO1", "NO2", "NO3G1", "NO3G2"],
        "Czech Republic": ["CZ1", "CZ2"],
        "Turkey": ["TU1", "TU2", "TU3B", "TU3K"],
        "Belgium": ["BE1", "BE2"],
        "Scotland": ["SC1", "SC2", "SC3", "SC4"],
        "Switzerland": ["CH1", "CH2"],
        "Finland": ["FI1", "FI2", "FI3A", "FI3B", "FI3C"],
        "Ukraine": ["UA1", "UA2"],
        "Romania": ["RO1", "RO2"],
        "Poland": ["PL1", "PL2", "PL3"],
        "Croatia": ["HR1", "HR2"],
        "Belarus": ["BY1", "BY2"],
        "Israel": ["IL1", "IL2"],
        "Iceland": ["IS1", "IS2", "IS3", "IS4"],
        "Cyprus": ["CY1", "CY2"],
        "Serbia": ["CS1", "CS2"],
        "Bulgaria": ["BG1", "BG2"],
        "Slovakia": ["SK1", "SK2"],
        "Hungary": ["HU1", "HU2"],
        "Kazakhstan": ["KZ1", "KZ2"],
        "Bosnia-Herzegovina": ["BA1"],
        "Slovenia": ["SI1", "SI2"],
        "Azerbaijan": ["AZ1"],
        "Ireland": ["IR1", "IR2"],
        "Latvia": ["LA1", "LA2"],
        "Georgia": ["GE1", "GE2"],
        "Kosovo": ["XK1"],
        "Albania": ["AL1"],
        "Lithuania": ["LT1", "LT2"],
        "North Macedonia": ["MK1"],
        "Armenia": ["AM1"],
        "Estonia": ["EE1", "EE2"],
        "Northern Ireland": ["NI1", "NI2"],
        "Malta": ["MT1"],
        "Luxembourg": ["LU1"],
        "Wales": ["WL1"],
        "Montenegro": ["MN1"],
        "Moldova": ["MD1"],
        "Färöer": ["FA1"],
        "Gibraltar": ["GI1"],
        "Andorra": ["AD1"],
        "San Marino": ["SM1"],
        "Brazil": ["BR1", "BR2", "BR3", "BRC", "BRGA"],
        "Mexico": ["MX1", "MX2"],
        "Argentina": ["AR1", "AR2", "AR3F", "AR5", "AR3", "AR4"],
        "USA": ["US1", "US2", "US3"],
        "Colombia": ["CO1", "CO2"],
        "Ecuador": ["EC1", "EC2"],
        "Paraguay": ["PY1", "PY2"],
        "Chile": ["CL1", "CL2"],
        "Uruguay": ["UY1", "UY2"],
        "Costa-Rica": ["CR1", "CR2"],
        "Bolivia": ["BO1"],
        "Guatemala": ["GT1", "GT2"],
        "Dominican Rep.": ["DO1"],
        "Honduras": ["HN1"],
        "Venezuela": ["VE1"],
        "Peru": ["PE1", "PE2"],
        "Panama": ["PA1"],
        "El Salvador": ["SV1"],
        "Japan": ["JP1", "JP2", "JP3"],
        "South-Korea": ["KR1", "KR2", "KR3"],
        "China": ["CN1", "CN2", "CN3"],
        "Iran": ["IA1", "IA2"],
        "Australia": ["AU1", "AU2V", "AU2NSW", "AU2Q", "AU2S", "AU2W"],
        "Saudi-Arabia": ["SA1", "SA2"],
        "Thailand": ["TH1", "TH2"],
        "Qatar": ["QA1", "QA2"],
        "United Arab Emirates": ["AE1", "AE2"],
        "Indonesia": ["ID1", "ID2"],
        "Jordan": ["JO1"],
        "Syria": ["SY1"],
        "Uzbekistan": ["UZ1"],
        "Malaysia": ["MY1", "MY2"],
        "Vietnam": ["VN1", "VN2"],
        "Iraq": ["IQ1"],
        "Kuwait": ["KW1"],
        "Bahrain": ["BH1"],
        "Myanmar": ["MM1"],
        "Palestine": ["PS1"],
        "India": ["IN1", "IN2"],
        "New Zealand": ["NZ1"],
        "Hong Kong": ["HK1", "HK2"],
        "Oman": ["OM1"],
        "Taiwan": ["TW1"],
        "Tajikistan": ["TJ1"],
        "Turkmenistan": ["TM1"],
        "Lebanon": ["LB1"],
        "Bangladesh": ["BD1"],
        "Singapore": ["SG1"],
        "Egypt": ["EG1", "EG2"],
        "Algeria": ["DZ1", "DZ2"],
        "Tunisia": ["TN1", "TN2"],
        "Morocco": ["MA1", "MA2"],
        "South-Africa": ["ZA1", "ZA2"],
        "Kenya": ["KE1", "KE2"],
        "Zambia": ["ZM1"],
        "Ghana": ["GH1"],
        "Nigeria": ["NG1"],
        "Uganda": ["UG1"],
        "Burundi": ["BI1"],
        "Rwanda": ["RW1"],
        "Cameroon": ["CM1"],
        "Tanzania": ["TZ1"],
        "Gambia": ["GM1"],
        "Sudan": ["SD1"]
    # Same dictionary as before
}

# Function to fetch table from website
def fetch_table(country, league, table_type="home"):
    url = f"https://www.soccer-rating.com/{country}/{league}/{table_type}/"
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        html_io = io.StringIO(str(soup))
        tables = pd.read_html(html_io, flavor="lxml")
        return tables[14] if tables else None
    except Exception as e:
        return None

# Streamlit UI with custom CSS
st.markdown("""
    <style>
        body {
            background-color: #f4f4f9;
            font-family: 'Arial', sans-serif;
        }
        .header {
            font-size: 32px;
            color: #3b5998;
            font-weight: bold;
            text-align: center;
        }
        .section-header {
            font-size: 20px;
            font-weight: 600;
            color: #007BFF;
        }
        .subsection-header {
            font-size: 18px;
            font-weight: 500;
            color: #5a5a5a;
        }
        .rating-table th {
            background-color: #007BFF;
            color: white;
            text-align: center;
        }
        .rating-table td {
            text-align: center;
        }
        .win-probability {
            color: #28a745;
            font-size: 18px;
            font-weight: 600;
        }
        .odds {
            color: #dc3545;
            font-size: 18px;
            font-weight: 600;
        }
        .slider {
            margin-top: 20px;
            padding: 10px;
            border-radius: 10px;
            background-color: #007BFF;
            color: white;
        }
        .button {
            background-color: #28a745;
            color: white;
            padding: 10px;
            border-radius: 8px;
            font-size: 16px;
        }
        .button:hover {
            background-color: #218838;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit header
st.markdown('<div class="header">⚽ Elo Ratings Odds Calculator</div>', unsafe_allow_html=True)

# Sidebar for selecting country and league
st.sidebar.header("⚽ Select Match Details")
selected_country = st.sidebar.selectbox("Select Country:", list(leagues_dict.keys()), index=0)
selected_league = st.sidebar.selectbox("Select League:", leagues_dict[selected_country], index=0)

# Fetch data if not available
if "home_table" not in st.session_state or "away_table" not in st.session_state or st.session_state.get("selected_league") != selected_league:
    if st.sidebar.button("Get Ratings", key="fetch_button", help="Fetch ratings and tables for selected country and league"):
        with st.spinner("The football ratings are warming up... almost ready!"):
            home_table = fetch_table(selected_country, selected_league, "home")
            away_table = fetch_table(selected_country, selected_league, "away")
            
            if isinstance(home_table, pd.DataFrame) and isinstance(away_table, pd.DataFrame):
                home_table = home_table.drop(home_table.columns[[0, 2, 3]], axis=1)
                away_table = away_table.drop(away_table.columns[[0, 2, 3]], axis=1)
                st.session_state["home_table"] = home_table
                st.session_state["away_table"] = away_table
                st.session_state["selected_league"] = selected_league
                st.success("Data fetched successfully!")
            else:
                st.error("Error fetching one or both tables. Please try again.")

# Display team selection and ratings
if "home_table" in st.session_state and "away_table" in st.session_state:
    # Main layout to display selected teams and odds
    st.markdown(f'<div class="section-header">⚽ Match Details</div>', unsafe_allow_html=True)
    
    # Dropdown for selecting teams
    home_team = st.selectbox("Select Home Team:", st.session_state["home_table"].iloc[:, 0])
    away_team = st.selectbox("Select Away Team:", st.session_state["away_table"].iloc[:, 0])

    # Fetching team ratings
    home_team_data = st.session_state["home_table"][st.session_state["home_table"].iloc[:, 0] == home_team]
    away_team_data = st.session_state["away_table"][st.session_state["away_table"].iloc[:, 0] == away_team]
    
    # Ratings for selected teams
    home_rating = home_team_data.iloc[0, 1]  
    away_rating = away_team_data.iloc[0, 1] 

     #alternative ratings for selected teams
    home  = 10**(home_rating/400)
    away = 10**(away_rating/400)
    
    # Calculating Win Probability
    home_win_prob = home/(home+away)
    away_win_prob = away/(away+home)
    
    # Display Ratings
    st.markdown(f'<div class="section-header">Selected Teams Ratings</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{home_team} Home Rating**")
        st.write(f"Rating: {home_rating}")
    with col2:
        st.markdown(f"**{away_team} Away Rating**")
        st.write(f"Rating: {away_rating}")

    # Display Win Probabilities
    st.markdown(f'<div class="section-header">Win Probability</div>', unsafe_allow_html=True)
    st.write(f"**Home Team Win Probability:** {home_win_prob:.2f}")
    st.write(f"**Away Team Win Probability:** {away_win_prob:.2f}")

    # Draw No Bet Odds Calculation
    home_draw_no_bet_odds = 1 / home_win_prob
    away_draw_no_bet_odds = 1 / away_win_prob
    st.markdown(f'<div class="section-header">Draw No Bet Odds</div>', unsafe_allow_html=True)
    st.write(f"**Home Team Draw No Bet Odds:** {home_draw_no_bet_odds:.2f}")
    st.write(f"**Away Team Draw No Bet Odds:** {away_draw_no_bet_odds:.2f}")

    # Determine default value for draw probability slider based on home_win_prob
    if 0.01 <= home_win_prob <= 0.10:
        default_draw_prob = 0.14
    elif 0.11 <= home_win_prob <= 0.19:
        default_draw_prob = 0.19
    elif 0.20 <= home_win_prob <= 0.25:
        default_draw_prob = 0.22
    elif 0.26 <= home_win_prob <= 0.35:
        default_draw_prob = 0.26
    elif 0.36 <= home_win_prob <= 0.45:
        default_draw_prob = 0.28
    elif 0.46 <= home_win_prob <= 0.70:
        default_draw_prob = 0.26
    elif 0.71 <= home_win_prob <= 0.75:
        default_draw_prob = 0.22
    elif 0.76 <= home_win_prob <= 0.80:
        default_draw_prob = 0.18
    elif 0.81 <= home_win_prob <= 0.90:
        default_draw_prob = 0.16
    elif 0.91 <= home_win_prob <= 0.95:
        default_draw_prob = 0.14
    elif 0.96 <= home_win_prob <= 0.99:
        default_draw_prob = 0.11
    else:
        default_draw_prob = 0.26  # Default value if no conditions are met
    
    # Slider for draw probability
    draw_prob_slider = st.slider("Select Draw Probability:", 0.1, 0.4, default_draw_prob, 0.01, key="draw_prob_slider")
    
    # Adjusting win probabilities with draw probability

    remaining_prob = 1 - draw_prob_slider
    home_win = home_win_prob*remaining_prob
    away_win = away_win_prob*remaining_prob


    home_odds = 1 / home_win if home_win > 0 else float('inf')
    away_odds = 1 / away_win if away_win > 0 else float('inf')
    draw_odds = 1 / draw_prob_slider if draw_prob_slider > 0 else float('inf')

    # Displaying 1X2 Odds
    st.markdown(f'<div class="section-header">1X2 Betting Odds</div>', unsafe_allow_html=True)
    st.write(f"**Home Win Odds**: {home_odds:.2f}")
    st.write(f"**Draw Odds**: {draw_odds:.2f}")
    st.write(f"**Away Win Odds**: {away_odds:.2f}")
