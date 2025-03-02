import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io
import math
import random

# Set page title and icon
st.set_page_config(page_title="Elo Ratings Odds Calculator", page_icon="odds_icon.png")



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
        "El-Salvador": ["SV1"],
        "Jamaica": ["JM1"],
        "Nicaragua": ["NC1"],
        "Canada": ["CA1"],
        "Haiti": ["HT1"],
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
        "Cambodia": ["KH1"],
        "Kyrgyzstan": ["KG1"],
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
    
}

# List of spinner messages
spinner_messages = [
    "Fetching the latest football ratings...",
    "Hold tight, we're gathering the data...",
    "Just a moment, crunching the numbers...",
    "Loading the football magic...",
    "Almost there, preparing the stats..."
]
# Function to fetch table from website
def fetch_table(country, league, table_type="home"):
    url = f"https://www.soccer-rating.com/{country}/{league}/{table_type}/"
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        html_io = io.StringIO(str(soup))
        tables = pd.read_html(html_io, flavor="lxml")
        
        # Get the rating table as before (using table index 14)
        rating_table = tables[14] if tables and len(tables) > 14 else None
        
        # Expected columns for the league table
        expected_columns = {"Home", "Away", "Home.4", "Away.4"}
        
        # Try to get the league table from possible indices first
        possible_indices = [28, 24, 23]
        league_table = None
        for idx in possible_indices:
            if tables and len(tables) > idx:
                candidate = tables[idx]
                candidate_cols = set(candidate.columns.astype(str))
                if expected_columns.issubset(candidate_cols):
                    league_table = candidate
                    break
        
        # If not found, loop through all tables to identify one by expected columns
        if league_table is None:
            for candidate in tables:
                candidate_cols = set(candidate.columns.astype(str))
                if expected_columns.issubset(candidate_cols):
                    league_table = candidate
                    break
                    
        return rating_table, league_table
    except Exception as e:
        return None, None


st.markdown("""\
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

# Explanation tooltip
if "data_fetched" not in st.session_state:
    st.info("Use the sidebar to select a country and league. Click 'Get Ratings' to fetch the latest data.")

# Sidebar for selecting country and league
st.sidebar.header("⚽ Select Match Details")
selected_country = st.sidebar.selectbox("Select Country:", list(leagues_dict.keys()), index=0)
selected_league = st.sidebar.selectbox("Select League:", leagues_dict[selected_country], index=0)

# Create two tabs
tab1, tab2 = st.tabs(["Odds Calculator & Match Analysis", "League Table"])

with tab1:
    # All existing calculation code goes here
    # Fetch data if not available
    if "home_table" not in st.session_state or "away_table" not in st.session_state or st.session_state.get("selected_league") != selected_league:
        if st.sidebar.button("Get Ratings", key="fetch_button", help="Fetch ratings and tables for selected country and league"):
            with st.spinner(random.choice(spinner_messages)):
                home_table, home_league_table = fetch_table(selected_country, selected_league, "home")
                away_table, away_league_table = fetch_table(selected_country, selected_league, "away")
                
                if isinstance(home_table, pd.DataFrame) and isinstance(away_table, pd.DataFrame):
                    home_table = home_table.drop(home_table.columns[[0, 2, 3]], axis=1)
                    away_table = away_table.drop(away_table.columns[[0, 2, 3]], axis=1)
                    st.session_state["home_table"] = home_table
                    st.session_state["away_table"] = away_table
                    st.session_state["league_table"] = home_league_table  # Store the league table
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

        # alternative ratings for selected teams
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
        col1, col2 = st.columns(2)  # Create two columns for layout
        with col1:
            st.write(f"**{home_team} Win Probability:** {home_win_prob:.2f}")
        with col2:
            st.write(f"**{away_team} Win Probability:** {away_win_prob:.2f}")

        # Draw No Bet Odds Calculation
        home_draw_no_bet_odds = 1 / home_win_prob
        away_draw_no_bet_odds = 1 / away_win_prob
        st.markdown(f'<div class="section-header">Draw No Bet Odds</div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)  # Create two columns for layout
        with col3:
            st.write(f"**{home_team} Draw No Bet Odds:** {home_draw_no_bet_odds:.2f}")
        with col4:
            st.write(f"**{away_team} Draw No Bet Odds:** {away_draw_no_bet_odds:.2f}")

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
        draw_prob_slider = st.slider("Select Draw Probability:", 0.05, 0.4, default_draw_prob, 0.01, key="draw_prob_slider")
        
        # Adjusting win probabilities with draw probability

        remaining_prob = 1 - draw_prob_slider
        home_win = home_win_prob*remaining_prob
        away_win = away_win_prob*remaining_prob


        home_odds = 1 / home_win if home_win > 0 else float('inf')
        away_odds = 1 / away_win if away_win > 0 else float('inf')
        draw_odds = 1 / draw_prob_slider if draw_prob_slider > 0 else float('inf')

        # Displaying 1X2 Odds
        st.markdown(f'<div class="section-header">1X2 Betting Odds</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)  # Create three columns for layout
        with col1:
            st.write(f"**{home_team} Win Odds**: {home_odds:.2f}")
        with col2:
            st.write(f"**Draw Odds**: {draw_odds:.2f}")
        with col3:
            st.write(f"**{away_team} Win Odds**: {away_odds:.2f}")
        
        
        
        
        if "league_table" in st.session_state and st.session_state["league_table"] is not None:
            league_table = st.session_state["league_table"]
        # Assuming team names are in the 2nd column (index 1) of the league table
            home_team_row = league_table[league_table.iloc[:, 1] == home_team]
            away_team_row = league_table[league_table.iloc[:, 1] == away_team]
            
            def extract_goals_parts(value):
                try:
                    parts = value.split(":")
                    if len(parts) >= 2:
                        goals_for = float(parts[0].strip())
                        goals_against = float(parts[1].strip())
                        return goals_for, goals_against
                    else:
                        return None, None
                except Exception as e:
                    return None, None

        # ----- Home Team Calculations -----
        if not home_team_row.empty:
            home_raw = home_team_row.iloc[0]["Home.4"]
            home_goals_for, home_goals_against = extract_goals_parts(home_raw)
            try:
                home_games = float(home_team_row.iloc[0]["Home"])
            except Exception as e:
                home_games = None
            home_goals_for_per_game = home_goals_for / home_games if home_goals_for is not None and home_games and home_games != 0 else None
            home_goals_against_per_game = home_goals_against / home_games if home_goals_against is not None and home_games and home_games != 0 else None
        else:
            home_goals_for_per_game = None
            home_goals_against_per_game = None

        # ----- Away Team Calculations -----
        if not away_team_row.empty:
            away_raw = away_team_row.iloc[0]["Away.4"]
            away_goals_for, away_goals_against = extract_goals_parts(away_raw)
            try:
                away_games = float(away_team_row.iloc[0]["Away"])
            except Exception as e:
                away_games = None
            away_goals_for_per_game = away_goals_for / away_games if away_goals_for is not None and away_games and away_games != 0 else None
            away_goals_against_per_game = away_goals_against / away_games if away_goals_against is not None and away_games and away_games != 0 else None
        else:
            away_goals_for_per_game = None
            away_goals_against_per_game = None

        # Display Goals For per Game
        st.markdown('<div class="section-header">Goals For per Game</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if home_goals_for_per_game is not None:
                st.write(f"**{home_team} Goals For per Game:** {home_goals_for_per_game:.2f}")
            else:
                st.write(f"**{home_team} Goals For per Game:** N/A")
        with col2:
            if away_goals_for_per_game is not None:
                st.write(f"**{away_team} Goals For per Game:** {away_goals_for_per_game:.2f}")
            else:
                st.write(f"**{away_team} Goals For per Game:** N/A")

        # Display Goals Against per Game
        st.markdown('<div class="section-header">Goals Against per Game</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if home_goals_against_per_game is not None:
                st.write(f"**{home_team} Goals Against per Game:** {home_goals_against_per_game:.2f}")
            else:
                st.write(f"**{home_team} Goals Against per Game:** N/A")
        with col2:
            if away_goals_against_per_game is not None:
                st.write(f"**{away_team} Goals Against per Game:** {away_goals_against_per_game:.2f}")
            else:
                st.write(f"**{away_team} Goals Against per Game:** N/A")
       
     
    # Calculate average league goals for and against
    if "league_table" in st.session_state and st.session_state["league_table"] is not None:
        league_table = st.session_state["league_table"]
        
        # Ensure the required columns exist
        if "Goals" in league_table.columns and "M" in league_table.columns:
            # Create new columns for Goals For (GF) and Goals Against (GA)
            league_table["GF"] = league_table["Goals"].apply(
                lambda x: float(x.split(":")[0].strip()) if isinstance(x, str) and ":" in x else None
            )
            league_table["GA"] = league_table["Goals"].apply(
                lambda x: float(x.split(":")[1].strip()) if isinstance(x, str) and ":" in x else None
            )
            
            # Calculate average goals for, against, and total per team
            avg_GF = league_table["GF"].mean()
            avg_GA = league_table["GA"].mean()
            avg_total = (league_table["GF"] + league_table["GA"]).mean()
            
            # Calculate the mean number of matches played from column 'M'
            avg_matches = league_table["M"].mean()
            
            # Calculate average goals per match: (GF+GA) per team divided by average matches
            avg_goals_per_match = avg_total / avg_matches if avg_matches and avg_matches != 0 else None
            
            st.markdown('<div class="section-header">League Average Goals</div>', unsafe_allow_html=True)
            
            
            if avg_goals_per_match is not None:
                st.write(f"**Average Goals per Match:** {avg_goals_per_match:.2f}")
            else:
                st.write("**Average Goals per Match:** N/A")
        else:
            st.write("The required columns ('Goals' and/or 'M') were not found in the league table.")

    # Calculate Expected Goals using the per game statistics
    home_expected_goals = None
    away_expected_goals = None

    if home_goals_for_per_game is not None and away_goals_against_per_game is not None:
        home_expected_goals = (home_goals_for_per_game + away_goals_against_per_game) / 2

    if away_goals_for_per_game is not None and home_goals_against_per_game is not None:
        away_expected_goals = (away_goals_for_per_game + home_goals_against_per_game) / 2

    total_expected_goals = None
    if home_expected_goals is not None and away_expected_goals is not None:
        total_expected_goals = ((home_expected_goals + away_expected_goals) + (avg_goals_per_match)) / 2

    # Display Expected Goals
    st.markdown('<div class="section-header">Expected Goals</div>', unsafe_allow_html=True)

    if total_expected_goals is not None:
            st.write(f"**Total Expected Goals:** {total_expected_goals:.2f}")
    else:
            st.write("**Total Expected Goals:** N/A")

    # Calculate team expected goals (xG) based on 1X2 odds and total expected goals using the provided formula

    if total_expected_goals is not None:
        # Sum of the probabilities for home win, draw, and away win
        total_probability = home_win_prob + draw_prob_slider + away_win_prob

        # Compute home and away xG based on the formula
        home_xG = total_expected_goals * ((home_win_prob + 0.5 * draw_prob_slider) / total_probability)
        away_xG = total_expected_goals * ((away_win_prob + 0.5 * draw_prob_slider) / total_probability)
    else:
        home_xG, away_xG = None, None

    # Display the calculated team expected goals (xG)
    st.markdown('<div class="section-header">Team Expected Goals (xG)</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if home_xG is not None:
            st.write(f"**{home_team} xG:** {home_xG:.2f}")
        else:
            st.write(f"**{home_team} xG:** N/A")
    with col2:
        if away_xG is not None:
            st.write(f"**{away_team} xG:** {away_xG:.2f}")
        else:
            st.write(f"**{away_team} xG:** N/A")

with tab2:
    # Display the league table
    if "league_table" in st.session_state and st.session_state["league_table"] is not None:
        league_table = st.session_state["league_table"]
        # Show only the specified columns
        league_table.rename(columns={'Unnamed: 0': 'Position'}, inplace=True)  # Rename the column
        # Display league table as text
        for index, row in league_table.iterrows():
            team_name = row[league_table.columns[1]]
            points = row["P."]  # Get the points from the last column
            if pd.notna(team_name):  # Check if team name is not NaN
                st.write(f"{row['Position']:.0f}. {team_name} - Points: {points}")  # Adjust the index if necessary
