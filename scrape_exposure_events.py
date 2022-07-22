import json
import re
import requests
from bs4 import BeautifulSoup

url = "https://basketball.exposureevents.com/youth-basketball-events"

payload = {
    "StateRegion":"Wisconsin",
    "StartDateString":"4/1/2022",
    "EndDateString":"7/5/2022",
    "Gender":"2",
    "EventType":"Tournament",
    "SearchToken":"",
    "InviteType":"-1",
    "Page":1,
    "sportType":"1"
}

headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
}

# response = requests.post(url, data=json.dumps(payload), headers=headers)
# json_response = response.json()

json_response = json.load(open('examples/exposure_event/tournament_list.json'))
page = json_response['Page']
page_size = json_response['PageSize']
total_count = json_response['Total']

print(f"Page: {page} | Page Size: {page_size} | Total Count {total_count}")

for tournament in json_response['Results']:
    tournament_link = tournament.get('Link')
    # tournament_link
    # https://basketball.exposureevents.com/176114/circuit-of-champions-chicago

    tournament_schedule_division_link = f"{tournament_link}/schedule"

    print(f"Fetch data for: {tournament.get('Name')} - {tournament_schedule_division_link}")
    tournament_schedule_division_html = requests.get(tournament_schedule_division_link)
    tournament_schedule_division_soup = BeautifulSoup(tournament_schedule_division_html.text, 'html.parser')
    division_links = tournament_schedule_division_soup.find_all('a', href=re.compile("#"))
    for division_link in division_links:
        division_name_parts = division_link.text.strip().split('\n')
        division_name = division_name_parts[0]
        division_data_bind = division_link.attrs['data-bind']
        if 'click: showDivision' in division_data_bind:
            division_id = re.search('(\d+)', division_data_bind).group(1)
            if len(division_id) > 0:
                print(f"Division Name: {division_name} | Division Id: {division_id}")
            else:
                print(f"Not a team link {division_name}")

            # https://basketball.exposureevents.com/177892/hardwood-hustle/eventgames?divisionId=605638
            division_games_url = f"{tournament_link}/eventgames?divisionId={division_id}"
            print(f"Fetch games for {division_games_url}")
            division_games_response = requests.get(division_games_url)
            division_games = division_games_response.json()
            # print(f"Division Games: {division_games}")
            for date_schedule in division_games:
                for game in date_schedule.get('Games', []):
                    # primary key
                    game.get('Id')
                    game.get('DateFormatted')
                    game.get('HomeTeamScoreDisplay')
                    game.get('AwayTeamScoreDisplay')
                    game.get('HomeTeamOtherScores')
                    game.get('AwayTeamOtherScores')
                    game.get('HomeTeamName')
                    game.get('AwayTeamName')
                    game.get('AwayTeamIsWinner')
                    game.get('HomeTeamIsWinner')
                    game.get('DivisionName')
                    # Persist to Database - 2 records: 1 for each team
                    print(f"{game['AwayTeamName']} at {game['HomeTeamName']}")

    # tournament_slug: /176114/circuit-of-champions-chicago/teams

    # Schedule Returns JSON: Request URL: https://basketball.exposureevents.com/177892/hardwood-hustle/eventgames?divisionId=605638


schedule_division_list_html = open('examples/exposure_event/schedule_division_list.html')
schedule_division_list_soup = BeautifulSoup(schedule_division_list_html, 'html.parser')
# Fetch all of the links
# filter out links that match the pattern: <tournament_slug>. The text in that link is the team name
links = schedule_division_list_soup.find_all('a', href=re.compile("#"))
print(f"Links: {len(links)} | {links}")


division_link = links[3]
# <a class="btn btn-light border-gray-darken h-100 d-block text-center text-dark text-decoration-none" data-bind="click: showDivision.bind($data, 605649)" href="#">
# <div class="display-8">BOYS 10u (2030) PLATINUM</div>
# <div class="total"><i>(9 teams)</i></div>
# </a>
division_name_parts = division_link.text.strip().split('\n')
print(f"Division Name Parts: {division_name_parts}")

division_name = division_name_parts[0]

division_data_binds = division_link.attrs['data-bind']
# click: showDivision.bind($data, 605639)

division_id = re.search('(\d+)', division_data_binds).group(1)
print(division_name)
print(division_data_binds)
print(division_id)