import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

## Links to main HTML Data files for a teams current season stats
data_sources = {
    "Cardinals" : "https://sports.yahoo.com/nfl/teams/arizona/stats/",
    "Falcons" : "https://sports.yahoo.com/nfl/teams/atlanta/stats/",
    "Ravens" : "https://sports.yahoo.com/nfl/teams/baltimore/stats/",
    "Bills" : "https://sports.yahoo.com/nfl/teams/buffalo/stats/",
    "Panthers" : "https://sports.yahoo.com/nfl/teams/carolina/stats/",
    "Bears" : "https://sports.yahoo.com/nfl/teams/chicago/stats/",
    "Bengals" : "https://sports.yahoo.com/nfl/teams/cincinnati/stats/",
    "Browns" : "https://sports.yahoo.com/nfl/teams/cleveland/stats/",
    "Cowboys" : "https://sports.yahoo.com/nfl/teams/dallas/stats/",
    "Broncos" : "https://sports.yahoo.com/nfl/teams/denver/stats/",
    "Lions" : "https://sports.yahoo.com/nfl/teams/detroit/stats/",
    "Packers" : "https://sports.yahoo.com/nfl/teams/green-bay/stats/",
    "Texans" : "https://sports.yahoo.com/nfl/teams/houston/stats/",
    "Colts" : "https://sports.yahoo.com/nfl/teams/indianapolis/stats/",
    "Jaguars" : "https://sports.yahoo.com/nfl/teams/jacksonville/stats/",
    "Chiefs" : "https://sports.yahoo.com/nfl/teams/kansas-city/stats/",
    "Raiders" : "https://sports.yahoo.com/nfl/teams/las-vegas/stats",
    "Chargers" : "https://sports.yahoo.com/nfl/teams/la-chargers/stats/",
    "Rams" : "https://sports.yahoo.com/nfl/teams/la-rams/stats/",
    "Dolphins" : "https://sports.yahoo.com/nfl/teams/miami/stats/",
    "Vikings" : "https://sports.yahoo.com/nfl/teams/minnesota/stats/",
    "Patriots" : "https://sports.yahoo.com/nfl/teams/new-england/stats/",
    "Saints" : "https://sports.yahoo.com/nfl/teams/new-orleans/stats/",
    "Giants" : "https://sports.yahoo.com/nfl/teams/ny-giants/stats/",
    "Jets" : "https://sports.yahoo.com/nfl/teams/ny-jets/stats/",
    "Eagles" : "https://sports.yahoo.com/nfl/teams/philadelphia/stats/",
    "Steelers" : "https://sports.yahoo.com/nfl/teams/pittsburgh/stats/",
    "49ers" : "https://sports.yahoo.com/nfl/teams/san-francisco/stats/",
    "Seahawks" : "https://sports.yahoo.com/nfl/teams/seattle/stats/",
    "Buccaneers" : "https://sports.yahoo.com/nfl/teams/tampa-bay/stats/",
    "Titans" :  "https://sports.yahoo.com/nfl/teams/tennessee/stats/",
    "Commanders" : "https://sports.yahoo.com/nfl/teams/washington/stats",
}

Titles = {
   0 : "Passing",
   1 : "Rushing",
   2 : "Receiving",
   3 : "Kicking",
   4 : "Returning",
   5 : "Punting",
   6 : "Defense",
   7 : "Division Comparison"
}

# Takes in a url, returns a list of relevant data frames as follows,
# Passing, Rushing, Receiving, Kicking, Returns, Punting, Defense
def scrape_tables_by_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    soup = BeautifulSoup(page_content, 'html.parser')
    tables = soup.find_all('table')
    return tables



def table_to_df(table):
    # Initialize an empty list to store rows
    data = []
    # Find the header row
    header_row = table.find('thead').find_all('tr')[0]
    headers = [th.text for th in header_row.find_all('th')]
    # Find all data rows
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        data.append([cell.text for cell in cells])
    # Create a DataFrame
    df = pd.DataFrame(data, columns=headers)
    return df

def generate_dataframes_from_tables(table_list):
    dataframes = []
    for table in table_list:
        dataframes.append(table_to_df(table))
    return dataframes

def dataframes_for_team(teamname):
    dataframes = []
    try:
        tables = scrape_tables_by_url(data_sources[teamname])
    except:
        print(f"Error downloading data for {teamname}. Exiting.")
        exit()
    dataframes = generate_dataframes_from_tables(tables)
    return dataframes

def print_team_dataframes(team_dfs):
    i = 0
    for key, value in Titles.items():
        print(value)
        print(team_dfs[key])
        print()

def save_df_to_csv(team_name, team_dfs):
    if (len(sys.argv) > 2):
        folder_path = "Data/"+team_name
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for key, value in Titles.items():
            if value == sys.argv[2]:
                team_dfs[key].to_csv(os.path.join("Data/"+team_name,f"{team_name}_{value}_stats.csv"), index = False)
    else:
        folder_path = "Data/"+team_name
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for key, value in Titles.items():
            team_dfs[key].to_csv(os.path.join("Data/"+team_name,f"{team_name}_{value}_stats.csv"), index = False)

def main():
    choice = input("Would you like to save these updated stats to a csv? (y/n): ")
    if len(sys.argv) > 1:
        team_dataframes = dataframes_for_team(sys.argv[1])
        if choice.lower() == 'y':
            save_df_to_csv(sys.argv[1],team_dataframes)
            print(f"{sys.argv[1]} Updated Successfully.")
    else:
        for key, value in data_sources.items():
            team_dataframes = dataframes_for_team(key)
            if choice.lower() == 'y':
                save_df_to_csv(key,team_dataframes)
                print(f"{key} Updated Successfully.")

if __name__ == '__main__':
    main()
