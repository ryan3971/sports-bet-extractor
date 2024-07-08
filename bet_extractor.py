import re

from config import extract_numbers
from abc import ABC, abstractmethod

# Abstract class for bet extractors
class BetExtractor(ABC):
    """
    This abstract class defines the structure for bet extractors.
    Bet extractors are responsible for extracting bet details from various sources.
    """
    @abstractmethod
    def __init__(self):
        """
        Initializes the bet extractor. This method is abstract and must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def extract_bet_details(self, bet_summary):
        """
        Extracts bet details from a bet summary.

        Parameters:
        - bet_summary: The summary of the bet from which details are to be extracted.

        This method is abstract and must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def process_extracted_details(self, bet_details):
        """
        Processes the extracted bet details.

        Parameters:
        - bet_details: The details of the bet that have been extracted.

        This method is abstract and must be implemented by subclasses.
        """
        pass
    
class Bet365(BetExtractor):
    """
    A concrete implementation of BetExtractor for the Bet365 betting platform.
    """
    def __init__(self):
        """
        Initializes the Bet365 bet extractor.
        """
        pass
    
    def extract_bet_details(self, bet_summary):
        """
        Extracts bet details from a Bet365 bet summary.

        Parameters:
        - bet_summary: The summary of the bet from Bet365 from which details are to be extracted.

        Returns:
        A dictionary containing the extracted bet details.
        """
        bet_details = {}
            
        # Extract date and time from the bet summary
        date_and_time = bet_summary.find('div', class_='h-BetSummary_DateAndTime').text.strip()
        bet_details['date_and_time'] = date_and_time
        
        # Placeholder for odds, to be extracted or calculated
        odds_holder = ''
        
        # Check for multiple selections in the bet, indicating a parlay bet
        multiple_selections = bet_summary.find('div', class_='h-BetBuilderMultipleSelections')
        if multiple_selections:
            # Extract the bet type from the header container of multiple selections
            bet_type = multiple_selections.find('div', class_='h-BetBuilderMultipleSelections_HeaderContainer').div.text.strip()
            # Extract all selections within the bet and their labels
            selections = multiple_selections.find_all('div', class_='h-BetBuilderSelection_Container')
            selection_labels = [selection.find('div', class_='h-BetBuilderSelection_SelectionLabel').text.strip() for selection in selections]
            
            # Extract odds for each selection from the odds label container
            odds_elements = multiple_selections.find('div', class_='h-BetBuilderMultipleSelections_OddsLabel').find_all('span')        
            odds_holder = [float(element.text.strip()) for element in odds_elements]
            
            odds = max(odds_elements, key=lambda x: float(x.text.strip())).text.strip()
                    
            fixture_label = multiple_selections.find('div', class_='h-BetBuilderMultipleSelections_FixtureLabel').text.strip()
        else:
            bet_type = "Single"
            selection = bet_summary.find('div', class_='h-BetSelection_Container')
            selection_labels = [selection.find('div', class_='h-BetSelection_Name').text.strip()]
            odds = selection.find('div', class_='h-BetSelection_Odds').text.strip()
            fixture_label = ""
        
        # Add extracted bet type and selections to the bet details dictionary
        bet_details['bet_type'] = bet_type
        bet_details['selection_labels'] = selection_labels
        # Add extracted odds to the bet details dictionary
        bet_details['odds'] = odds
        bet_details['fixture_label'] = fixture_label
        bet_details['odds_holder'] = odds_holder
        
        # Extract stake and return information
        stake = bet_summary.find('div', class_='h-StakeDescription_Text').text.strip()
        bet_details['stake'] = stake#extract_numbers(stake)
        
        # Extract the wager and return amount
        try:
            # this is not a bonus bet
            wager = bet_summary.find('div', class_='h-StakeReturnSection_StakeContainer').text.strip()
            ret = bet_summary.find('div', class_='h-StakeReturnSection_ReturnText').text.strip()
            bonus_bet = False
        except:
            # this is a bonus bet
            wager = bet_summary.find('div', class_='h-StakeReturnSectionIPOffer_StakeDetails').text.strip()
            ret = bet_summary.find('div', class_='h-StakeReturnSectionIPOffer_ReturnContainer').text.strip()
            bonus_bet = True        
                
        # Check for super boost
        boost = bet_summary.find('div', class_='h-WinningsBoostBadge_BoostLabel') or bet_summary.find('div', class_='h-BetBoostLabel h-BetBoostLabel-superboost')
        if boost:
            # strip text and replace line breaks with a space
            bet_details['boost'] = boost.text.strip().replace('\n', ' ')
        else:
            bet_details['boost'] = None
            
        bet_details['wager'] = wager
        bet_details['return'] = ret
        bet_details['bonus_bet'] = bonus_bet
            
        return bet_details
    
    def process_extracted_details(self, bet_details):
        """
        Processes the extracted bet details specific to Bet365.

        This method takes the raw bet details extracted from the Bet365 bet summary,
        and processes them to format or calculate additional information that may be
        necessary for further use, such as calculating potential winnings or formatting
        the date and time.

        Parameters:
        - bet_details: A dictionary containing the details of the bet extracted from the Bet365 summary.

        Returns:
        A dictionary with the processed bet details, which may include additional keys
        for calculated or formatted information.
        """
        bet_output = {}
        boost = ''
    
        # convert the date format from "dd/mm/yyyy hh:mm" to "yyyy-mm-dd hh:mm"
        date_time = bet_details['date_and_time']
        date_time = date_time.split(' ')
        date = date_time[0].split('/')
        time = date_time[1]
        date = date[2] + '-' + date[0] + '-' + date[1]
        date_time = date + time

        # save just the date
        bet_output['date'] = date
        
        # use the date and time to create a unique bet ID
        bet_id = date_time.replace(' ', '_')
        bet_output['bet_id'] = bet_id.replace(':', '').replace('-', '')
        
        # set the bookmaker name
        bookmaker = 'bet365'
        bet_output['bookmaker'] = bookmaker
        
        # set the sport to nothing for now
        bet_output['sport'] = ''
        
        # get the selection labels, and convert the list into a numbered string separated by a line break; if there is only 1 selection, then just use that
        selection_labels = bet_details['selection_labels']
        if len(selection_labels) > 1:
            selection_labels = [str(i+1) + '. ' + selection for i, selection in enumerate(selection_labels)]
            selection_labels = '\n'.join(selection_labels)
        else:
            selection_labels = selection_labels[0]
            
        bet_output['selection'] = selection_labels
        
        # depending on the selection length, we can set the bet type
        selection_label_items = len(bet_details['selection_labels'])
        if selection_label_items == 2:
            bet_output['bet_type'] = 'Multi Bet - 2 legs'
        elif selection_label_items == 3:
            bet_output['bet_type'] = 'Multi Bet - 3 legs'
        elif selection_label_items >= 4:
            bet_output['bet_type'] = 'Multi Bet - 4+ legs'
        else:
            bet_output['bet_type'] = ''
            
        # also check for boost if it's a single leg
        if bet_details['boost'] and "boost" in bet_details['boost'].lower():
            boost = 'Boost'
        
        bet_output['boost'] = boost
        
        # get the stake and extract the number (should be 1 number only)
        bet_output['wager'] = extract_numbers(bet_details['wager'])[0]
        
        # get whether it is a bonus bet or not
        if bet_details['bonus_bet']:
            bet_output['bonus_bet'] = 'Y'
        else:
            bet_output['bonus_bet'] = 'N'
        
        # get the odds and extract the number
        bet_output['odds'] = bet_details['odds']
        
        # get the return and extract the number (should be 1 number only)
        returned = float(extract_numbers(bet_details['return'])[0])
        print(bet_output['wager'], returned)

        # if the return is 0, then the bet is a loss. If it is not 0, then the bet is a win. Else, the bet is pending
        if returned == 0:
            bet_output['bet_status'] = 'N'
        # check if the bet was cashed out (i.e., it was voided)
        elif float(bet_output['wager']) == float(returned):
            bet_output['bet_status'] = 'R'
        elif returned > 0:
            bet_output['bet_status'] = 'Y'
        else:
            bet_output['bet_status'] = 'P'
            
        # we can use the fixture as is
        bet_output['fixture'] = bet_details['fixture_label']
        
        return bet_output
    
class Fanduel(BetExtractor):
    """
    A concrete implementation of BetExtractor for the Fanduel betting platform.
    
    This class is responsible for extracting and processing bet details specific to the Fanduel platform.
    It implements the abstract methods defined in the BetExtractor abstract class to provide functionality
    for initializing the extractor, extracting bet details from a bet summary, and processing those details.
    """
    def __init__(self):
        """
        Initializes the Fanduel bet extractor.
        
        This constructor can be expanded to include initialization of resources or configurations
        specific to handling Fanduel bet summaries.
        """
        pass
    
    def extract_bet_details(self, bet_summary):
        """
        Extracts bet details from a Fanduel bet summary.

        This method parses the bet summary provided as input to extract relevant details
        such as the date and time of the bet, the bet type, selections, and odds. The
        extracted details are returned in a dictionary format.

        Parameters:
        - bet_summary: The summary of the bet from Fanduel from which details are to be extracted.

        Returns:
        A dictionary containing the extracted bet details.
        """
        bet_details = {}
    
        # Extract bet status
        bet_status = bet_summary['class'][1].split('-')[-1]
        bet_details['bet_status'] = bet_status
        
        # Extract bet type
        bet_type = bet_summary['class'][3]
        bet_details['bet_type'] = bet_type
        
        # Extract the event name and time
        event_name = bet_summary.select_one('.eventname')
        if event_name:
            bet_details['event_name'] = bet_summary.select_one('.eventname').get_text(strip=True)
        else:
            bet_details['event_name'] = None
        
        time_status = bet_summary.select_one('.time-player .time') or bet_summary.select_one('.time')
        if time_status:
            bet_details['time_status'] = time_status.get_text(strip=True)
        
        # Extract leg information
        legs = []
        leg_names = bet_summary.select('.leg-name')
        leg_subs = bet_summary.select('.leginfo-sub .first')
        
        for name, sub in zip(leg_names, leg_subs):
            legs.append({
                'leg_name': name.get_text(strip=True),
                'leg_info': sub.get_text(strip=True)
            })
        
        bet_details['legs'] = legs
        
        # Extract odds
        odds = bet_summary.select_one('.leginfo-odds') or bet_summary.select_one('.betodds .value')
        if odds:
            bet_details['odds'] = odds.get_text(strip=True)
        
        # Extract total wager
        wager = bet_summary.select_one('.betstake .value span')
        if wager:
            bet_details['total_wager'] = wager.get_text(strip=True)
        
        # Extract return
        bet_return = bet_summary.select_one('.betreturn .value span')
        if bet_return:
            bet_details['bet_return'] = bet_return.get_text(strip=True)
        
        # Extract bet ID
        bet_id = bet_summary.select_one('.bet-id span:last-child')
        if bet_id:
            bet_details['bet_id'] = bet_id.get_text(strip=True)
        
        # Extract placed time
        placed_time = bet_summary.select_one('.time span:last-child')
        if placed_time:
            bet_details['placed_time'] = placed_time.get_text(strip=True)
        
        # Extract bonus bet information
        bonus_bet = bet_summary.select_one('.bonus-bets')
        if bonus_bet:
            bonus_amount = bonus_bet.select_one('.bonus-amount')
            bonus_text = bonus_bet.select_one('.bonus-text')
            if bonus_amount and bonus_text:
                bet_details['bonus_bet'] = {
                    'bonus_amount': bonus_amount.get_text(strip=True),
                    'bonus_text': bonus_text.get_text(strip=True)
                }
        else:
            bet_details['bonus_bet'] = None
        
        return bet_details
    
    def process_extracted_details(self, bet_details):
        """
        Processes the extracted bet details specific to Fanduel.

        This method takes the raw bet details extracted from the Fanduel bet summary,
        and processes them to format or calculate additional information that may be
        necessary for further use. This could include formatting the date and time,
        calculating potential winnings based on odds and stake, or any other processing
        specific to the Fanduel platform.

        Parameters:
        - bet_details: A dictionary containing the details of the bet extracted from the Fanduel summary.

        Returns:
        A dictionary with the processed bet details, which may include additional keys
        for calculated or formatted information.
        """
        bet_output = {}
        boost = ''

        # store the retrieved bet ID
        bet_output['bet_id'] = bet_details['bet_id'].strip('#')
        
        # get the date and time
        date_time = bet_details['placed_time']
        
        # extract the date from the date and time, parse the date string into a datetime object, and convert the datetime object to the desired format
        date = date_time.split(' ')[0:3]
        date = date[1].strip(',') + '-' + date[0] + '-' + date[2]
        bet_output['date'] = date
        
        # set the bookmaker name
        bookmaker = 'FanDuel'
        bet_output['bookmaker'] = bookmaker
            
        # set the sport to nothing for now
        bet_output['sport'] = ''
        
        # get the selection labels, and convert the list into a numbered string separated by a line break; if there is only 1 selection, then just use that
        legs = bet_details['legs']
        if len(legs) > 1:
            # if there are multiple legs, then extract the leg names and leg info
            selection_labels = []
            for leg in legs:
                leg_name = leg['leg_name']
                leg_info = leg['leg_info']
                selection_labels.append(leg_name + ' - ' + leg_info)
                
            # Number the selections
            selection_labels = [str(i+1) + '. ' + selection for i, selection in enumerate(selection_labels)]
            selection_labels = '\n'.join(selection_labels).strip("\"")

        else:
            leg_name = legs[0]['leg_name']
            leg_info = legs[0]['leg_info']
            
            # remove all text after a ( in the leg name
            leg_name = re.sub(r' \(.*\)', '', leg_name).strip()
                    
            # also check for boost if it's a single leg
            if "boost" in leg_info.lower():
                boost = 'Boost'
                selection_labels = leg_name
                # bets that are not boosted have useful information in the leg info
            else:
                selection_labels = leg_name + ' - ' + leg_info
                
        bet_output['selection'] = selection_labels.replace(',', ';')    # replace , with ; (since we are saving to csv file)
        bet_output['boost'] = boost
        
        # depending on the selection length, we can set the bet type
        if len(legs) == 2:
            bet_output['bet_type'] = 'Multi Bet - 2 legs'
        elif len(legs) == 3:
            bet_output['bet_type'] = 'Multi Bet - 3 legs'
        elif len(legs) >= 4:
            bet_output['bet_type'] = 'Multi Bet - 4+ legs'
        else:
            bet_output['bet_type'] = ''
        
        # get the stake and extract the number (should be 1 number only)
        bet_output['wager'] = extract_numbers(bet_details['total_wager'])[0]
        
        # get whether it is a bonus bet or not
        if bet_details['bonus_bet']:
            bet_output['bonus_bet'] = 'Y'
        else:
            bet_output['bonus_bet'] = 'N'
        
        
        # get the odds and extract the number
        bet_output['odds'] = bet_details['odds']
        
        # get the return and extract the number (should be 1 number only)
        returned = float(extract_numbers(bet_details['bet_return'])[0])
        
        # if the return is 0, then the bet is a loss. If it is not 0, then the bet is a win. Else, the bet is pending
        if returned == 0:
            bet_output['bet_status'] = 'N'
        elif returned > 0:
            bet_output['bet_status'] = 'Y'
        else:
            bet_output['bet_status'] = 'P'
            
        # set fixture to eveent name
        bet_output['fixture'] = bet_details['event_name']
        
        return bet_output