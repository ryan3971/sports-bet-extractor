config.json
1) Add OpenAPI key
2) include all bookmakers you want to extract data from

Fanduel:
1) Open Settled bets page
2) inspect elements
3) search for "stmnt-bets" (quotes included)
4) Copy the found element (the top element, the one that houses all the bets; hover over to tell which)
5) Create a .html file and paste contents to it

Bet365:
1) Navigate to Account History
2) Inspect elements
3) Search for "hl-SummaryRenderer_Container " (quotes and space included)
4) Copy the found element (the top element, the one that houses all the bets; hover over to tell which)
5) Create a .html file and paste contents to it

Copy to Excel doc:
- keep formatting when pasting so multi line entries show over several lines (easier to read)

Areas that could be improved:
- classification of the bets (need a list of potential bet types)
- Improve generation in general (can provide examples)
