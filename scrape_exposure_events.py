import json
import pdb
import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://basketball.exposureevents.com/youth-basketball-events"

SPORT_CODE_BASKETBALL = 1
GENDER_CODE_BOY = 1
GENER_CODE_GIRL = 2

# json_response = json.load(open('examples/exposure_event/tournament_list.json'))

def process(start_date, end_date):
    page = 1
    returned_records = -1
    total_records = 0

    while returned_records < total_records:
        tournament_json = get_list_of_tournaments_by_page(
            gender_code=GENER_CODE_GIRL,
            page=int(page),
            start_date=start_date,
            end_date=end_date
        )
        page = tournament_json['Page']
        page_size = tournament_json['PageSize']
        returned_records = int(page) * int(page_size)
        total_records = tournament_json['Total']
        print(f"Page: {page} | Page Size: {page_size} | Total Count {total_records}")
        # parse_tournament_json(tournament_json=tournament_json)
        page += 1

def get_list_of_tournaments_by_page(gender_code, page, start_date, end_date, ):
    payload = {
        "StateRegion": "Wisconsin",
        "StartDateString": start_date,
        "EndDateString": end_date,
        "Gender": str(gender_code),
        "EventType": "Tournament",
        "SearchToken": "",
        "InviteType": "-1",
        "Page": int(page),
        "sportType": str(SPORT_CODE_BASKETBALL)
    }
    response = requests.post(BASE_URL, data=json.dumps(payload), headers=json_headers())
    json_response = response.json()
    return json_response

def parse_tournament_json(tournament_json):
    for tournament in tournament_json['Results']:
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



def json_headers():
    return {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
    }

if __name__ == "__main__":
    start_date = "4/1/2022"
    end_date = "7/31/2022"
    process(start_date=start_date, end_date=end_date)

# schedule_division_list_html = open('examples/exposure_event/schedule_division_list.html')
# schedule_division_list_soup = BeautifulSoup(schedule_division_list_html, 'html.parser')
# # Fetch all of the links
# # filter out links that match the pattern: <tournament_slug>. The text in that link is the team name
# links = schedule_division_list_soup.find_all('a', href=re.compile("#"))
# print(f"Links: {len(links)} | {links}")


# division_link = links[3]
# # <a class="btn btn-light border-gray-darken h-100 d-block text-center text-dark text-decoration-none" data-bind="click: showDivision.bind($data, 605649)" href="#">
# # <div class="display-8">BOYS 10u (2030) PLATINUM</div>
# # <div class="total"><i>(9 teams)</i></div>
# # </a>
# division_name_parts = division_link.text.strip().split('\n')
# print(f"Division Name Parts: {division_name_parts}")

# division_name = division_name_parts[0]

# division_data_binds = division_link.attrs['data-bind']
# # click: showDivision.bind($data, 605639)

# division_id = re.search('(\d+)', division_data_binds).group(1)
# print(division_name)
# print(division_data_binds)
# print(division_id)