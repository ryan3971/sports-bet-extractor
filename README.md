# Bet Extractor

This repository contains scripts to extract and process betting data. The key components include a configuration file, a bet extraction script, and a script to run the bet extraction process. 

**Note:**
The project was designed to produce data that could easily be imported into the following worksheet:
https://www.aussportsbetting.com/tools/betting-tracker-excel-worksheet/
Open the linked workbook and run the provided VBA script, import_data.bas to import the sport betting information produced from running this project.

## Files

- `config.py`
- `bet_extractor.py`
- `run_bet_extractor.py`

### 1. `config.py`

This file contains the configuration settings required by the other scripts. It defines parameters such as file paths, database connections, API keys, and any other necessary settings.

**Key Components:**
- Configuration settings
- Path definitions
- API keys and authentication tokens

### 2. `bet_extractor.py`

This script handles the core functionality of extracting betting data. It contains functions and classes to parse and process the data from various sources.

**Key Components:**
- Data extraction functions
- Data parsing and processing
- Error handling

### 3. `run_bet_extractor.py`

This script is the main entry point to run the bet extraction process. It uses the configurations defined in `config.py` and the functions in `bet_extractor.py` to perform the extraction and processing tasks.

**Key Components:**
- Initialization of the extraction process
- Integration with configuration settings
- Execution of data extraction and processing

## Usage

1. **Setup Configuration:**
   - Update the `config.py` file with the necessary configuration settings, such as file paths, API keys, and database connections.

2. **Run Extraction:**
   - Execute the `run_bet_extractor.py` script to start the bet extraction process.
   - Example: `python run_bet_extractor.py`

## Requirements

- Python 3.x
- Required libraries (specify the libraries used in your scripts)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/bet_extractor.git
   cd bet_extractor
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Update the configuration file (`config.py`) with your settings.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
