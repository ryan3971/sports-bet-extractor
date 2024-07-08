from bs4 import BeautifulSoup
from pprint import pprint
from config import LLM

from bet_extractor import Bet365, Fanduel
import csv

# specify the bookmaker to extract the bets from - either 'fanduel' or 'bet365'
bookmaker = 'bet365'

# specify the html file to extract the bets from
if bookmaker == 'fanduel':
    html_file = "fanduel.html"
    bet_extractor = Fanduel()
    csv_file = "fanduel.csv"
elif bookmaker == 'bet365':
    html_file = "bet365.html"
    bet_extractor = Bet365()
    csv_file = "bet365.csv"

# Read the HTML content from the file
with open(html_file) as f:
    html_content = f.read()
    
# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract all bets
if bookmaker == 'fanduel':
    bet_summaries = soup.select('.stmnt-bet')
elif bookmaker == 'bet365':
    bet_summaries = soup.find_all('div', class_='h-BetSummary')

# Extract the details of each bet
all_bet_details = [bet_extractor.extract_bet_details(bet_summary) for bet_summary in bet_summaries]


# Print the extracted bet details in a nicely formatted way
pprint(all_bet_details)

# save the extracted bet details to a csv file - this can be used to check the extracted details before processing them
csv_columns = all_bet_details[0].keys()

# save the extracted bet details to a csv file in a specific order of columns
try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        
        # Write the data to the CSV file row by row
        
        for data in all_bet_details:
            writer.writerow(data)
except IOError:
    print("I/O error")
    
# define the llm object
llm = LLM()
    
# Process the extracted details
processed_bet_details = [bet_extractor.process_extracted_details(bet_details) for bet_details in all_bet_details]
processed_bet_details = [llm.run_llm(bet_details) for bet_details in processed_bet_details]

# save the extracted bet details to a csv file in a specific order of columns
if bookmaker == 'fanduel':
    csv_file = "fanduel_processed.csv"
elif bookmaker == 'bet365':
    csv_file = "bet365_processed.csv"

# define the new order of columns
new_csv_columns = ["Date", 'Notes', 'Bookmaker', 'Sport / League', 'Selection', 'Bet Type', 'My Variable', 'Fixture / Event', 'Stake', 'Odds (US)','BB', 'Win']

# rename the columns to match the new order
for data in processed_bet_details:
    data['Date'] = data.pop('date')
    data['Notes'] = data.pop('bet_id')
    data['Bookmaker'] = data.pop('bookmaker')
    data['Sport / League'] = data.pop('sport')
    data['Selection'] = data.pop('selection')
    data['Bet Type'] = data.pop('bet_type')
    data['My Variable'] = data.pop('boost')
    data['Fixture / Event'] = data.pop('fixture')
    data['Stake'] = data.pop('wager')
    data['Odds (US)'] = data.pop('odds')
    data['BB'] = data.pop('bonus_bet')
    data['Win'] = data.pop('bet_status')

# save the processed bet details to a csv file
try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=new_csv_columns)
        writer.writeheader()
        
        # Write the data to the CSV file row by row
        
        for data in processed_bet_details:
            writer.writerow(data)
        
except IOError:
    print("I/O error")