from bs4 import BeautifulSoup
import requests
import re


def get_league_scrape():
    url = "https://www.pathofexile.com/"
    headers = {'user-agent': 'Mozilla/5.0'}
    req = requests.get(url, headers = headers)
    soup = BeautifulSoup(req.text, "html.parser")
    leagues = [x.text for x in soup.find("li", {"id" : "nav-events"}).find("ul")]
    leagues = leagues[3:]
    leagues = [x for x in leagues if not(re.match("^SSF.*", x))]

    print("Choose a league:")
    for index, league in enumerate(leagues):
        print("{index}: {league}".format(index=index, league=league))
    while True:
        user_league_choice = input()
        # Checks for if input is correct or not (int between 0 and number of leagues)
        if user_league_choice.isnumeric() and 0 <= int(user_league_choice) and int(user_league_choice) < len(
                leagues):
            user_league_choice = int(user_league_choice)
            print("You have chosen {league}.".format(league=leagues[user_league_choice]))
            return leagues[user_league_choice]
        else:
            print("Error: Invalid choice.")