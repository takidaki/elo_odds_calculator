This is a Streamlit-based web application that calculates betting odds (1X2) based on Elo ratings for soccer teams. The app allows users to select a country and league, fetch the teams' Elo ratings, and compute the win probability for both home and away teams, as well as odds for the 1X2 betting market.

Features
Select a country and league to fetch Elo ratings of home and away teams.
Calculate win probabilities based on Elo ratings.
Calculate Draw No Bet odds for both teams.
Choose a draw probability between 0.15 and 0.4 to calculate final 1X2 betting odds.
Clean and user-friendly interface with dynamic dropdowns and interactive sliders.
Requirements
To run this application, you'll need to have Python 3.x installed, along with the following dependencies:

streamlit: for creating the web app interface.
pandas: for handling data manipulation.
requests: for fetching data from external websites.
beautifulsoup4: for parsing HTML content from the fetched websites.
lxml: for parsing HTML tables.
You can install the necessary libraries using pip:

bash
Copy
Edit
pip install streamlit pandas requests beautifulsoup4 lxml
How to Run
Clone the repository to your local machine:

bash
Copy
Edit
git clone https://github.com/takidaki/elo_odds_calculator.git
Navigate into the project folder:

bash
Copy
Edit
cd elo_odds_calculator
Run the Streamlit app:

bash
Copy
Edit
streamlit run odds.py
Open your web browser and navigate to the local URL provided by Streamlit (typically http://localhost:8501).

How it Works
Country and League Selection:

Select a country from the dropdown menu. Once a country is selected, the corresponding leagues will be populated dynamically.
Fetching Team Data:

Once you've selected the country and league, the app fetches the latest team Elo ratings from a website.
Win Probability Calculation:

The win probability for both the home and away teams is calculated using their Elo ratings. 
​
 
Draw No Bet Odds:

Based on the calculated win probabilities, the Draw No Bet odds for both teams are displayed.
1X2 Betting Odds:

You can adjust the draw probability using a slider (between 0.15 and 0.4). Based on the selected draw probability, the app recalculates the 1X2 odds.
User Interface:

The interface provides dynamic dropdowns, showing data relevant to the selected country and league.
A progress spinner will show while the app fetches the data.

Demo

Future Improvements
Add more countries and leagues.
Include additional betting markets (e.g., Over/Under, Correct Score).
Allow users to compare multiple teams at once.
Add data visualization for Elo ratings and betting odds.
Contributing
Contributions are welcome! If you want to improve this project, feel free to fork the repository, make your changes, and submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
The soccer team data is fetched from the website Soccer-Rating.com.
Inspired by the power of Elo ratings in predicting soccer match outcomes.
