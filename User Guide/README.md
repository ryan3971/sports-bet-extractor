### Instructions for Setting Up and Using Bet Extractor

#### Configuration (`config.json`)
1. **Add OpenAPI Key**
   - Ensure you include your OpenAPI key in the `config.json` file.

2. **Include Bookmakers**
   - List all bookmakers you want to extract data from in the `config.json` file.

#### Fanduel:
1. Open the Settled Bets page on Fanduel.
2. Right-click on the page and select "Inspect" to open the developer tools.
3. Use the search function within the developer tools to find the element by searching for `"stmnt-bets"` (include quotes).
4. Locate the top element that contains all the bets (you can hover over the elements to identify the correct one).
5. Copy the entire HTML content of this element.
6. Create an `.html` file and paste the copied content into this file.

#### Bet365:
1. Navigate to the Account History page on Bet365.
2. Right-click on the page and select "Inspect" to open the developer tools.
3. Use the search function within the developer tools to find the element by searching for `"hl-SummaryRenderer_Container "` (include quotes and space).
4. Locate the top element that contains all the bets (you can hover over the elements to identify the correct one).
5. Copy the entire HTML content of this element.
6. Create an `.html` file and paste the copied content into this file.

#### Copying to Excel:
- When copying the extracted data to an Excel document, ensure you keep the formatting. This way, multi-line entries will display over several lines, making them easier to read.

#### Areas for Improvement:
- **Classification of Bets:** Develop a comprehensive list of potential bet types to improve classification.
- **General Improvements:** Enhance the overall process and accuracy of data extraction and processing. (You can provide examples to guide these improvements).
