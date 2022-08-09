# Tableau Dashboard for Fantasy Premier League (FPL) Mini-League
## About the Project
This project was designed to provide the data for the FPL Mini-League Dashboard, which aims to monitor monthly and overall winning teams, and show the 'factors' to winning in FPL - namely through transfers and squad value.

## Development
The data is compiled and processed in the following method:
- The Fantasy Premier League API is the data source
- Data is extracted, transformed and stored on Google Sheets using Python
  - Packages used: Pandas, requests, gspread and gspread_pandas
- Python script is run daily at 12pm AEST using Cron on a Raspberry Pi 4B
- Tableau Public is used to vizualise the data: 22/23 season version can be found [here](https://public.tableau.com/views/FPLMini-LeagueStatistics2223/Overview?:language=en-GB&:display_count=n&:origin=viz_share_link).
