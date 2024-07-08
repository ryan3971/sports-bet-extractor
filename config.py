# Import necessary modules and classes from langchain_core and langchain_openai
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

# Standard library imports
import enum
import os
import re

# Data Models Section
class Classification(BaseModel):
    """
    A Pydantic model representing a classification of a bet.
    
    Attributes:
    - sport: A string indicating the sport category of the bet. It is restricted to a predefined list of sports.
    - bet_type: A string indicating the type of bet. It is restricted to a predefined list of bet types.
    """
    # Enumerated field for sport category, ensuring only valid sports are used
    sport: str = Field(..., enum=['NBA',
                                'MLB',
                                'NHL',
                                'Tennis',
                                'Soccer',
                                'Golf',
                                'NFL',
                                'UFC',
                                'Formula 1',
                                'Unknown'
                                ])
     
    # Enumerated field for bet type, ensuring only valid bet types are used                       
    bet_type: str = Field(..., enum=['Winner',
                                'Head to Head',
                                'Not to Win',
                                'Doubles',
                                'Triples',
                                'Over / Under',
                                'No Run First Inning',
                                'To Hit Home Run',
                                'Unknown'
                               ])
    
# Prompt Template Section

# Define a prompt template for extracting the desired information from the provided information
tagging_prompt = ChatPromptTemplate.from_template(
"""
Extract the desired information from the provided information.
Only extract the properties mentioned in the 'Classification' function.

Text:
{input}
"""
)
class LLM():
    """
    The LLM (Language Learning Model) class is designed to initialize and configure language model settings,
    specifically for integrating OpenAI's language models into the application. It sets up the necessary
    environment variables for API access and configures the language model with specific parameters for
    generating structured output based on a predefined Pydantic model.
    
    Attributes:
    - chain: A pipeline that combines a prompt template with the language model to process input text
             and generate structured output.
    """
    def __init__(self):
        """
        Initializes the LLM class by setting up the necessary environment variables for API access
        and configuring the language model with specific parameters.
        
        The language model is configured to use a specific model version (e.g., "gpt-3.5-turbo-0125"),
        with a temperature setting of 0 for deterministic outputs. It is further configured to produce
        structured output that conforms to the 'Classification' Pydantic model.
        
        The 'chain' attribute is set up as a pipeline that first applies a prompt template to the input text
        to guide the extraction of desired information. The processed input is then passed to the configured
        language model to generate structured output. This setup allows for flexible and efficient processing
        of text to extract specific information as defined in the 'Classification' model.
        """

        # Initialize the language model with specific parameters
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125").with_structured_output(
            Classification
        )
        # Initialize the Tavily Search API Retriever
        # retriever = TavilySearchAPIRetriever(k=3)
        # self.chain = (
        #     RunnablePassthrough.assign(context=(lambda x: x["input"]) | retriever)
        #     | tagging_prompt
        #     | llm
        # )
        
        self.chain = tagging_prompt | llm

    def run_llm(self, bet_output):
        """
        Runs the LLM (Low Level Model) on the given `bet_output` and updates the `bet_output` dictionary with the results.

        Parameters:
        - bet_output (dict): A dictionary containing information about the bet.

        Returns:
        - dict: The updated `bet_output` dictionary.

        Raises:
        - Exception: If an error occurs during the execution of the LLM.

        """
        try:
            # all selections from here are single bets
            selection = bet_output['selection']

            output = self.chain.invoke({"input": selection})

            bet_output['sport'] = output.sport

            # skip the Multi bets
            if bet_output['bet_type'] == '':
                bet_output['bet_type'] = output.bet_type

            print(f"Input: {selection}")
            print(f"Output: {output}")
            print()

        except Exception as e:
            print(f"Error: {e}")

        return bet_output
    
# Helper functions for extracting numbers from strings
def extract_numbers(string):
    if string is None:
        return None
    
    pattern = r'(?<=\$)\d+(?:\.\d+)?|(?<!\d)\d+(?:\.\d+)?(?=%)'
    numbers = re.findall(pattern, string)
    return numbers