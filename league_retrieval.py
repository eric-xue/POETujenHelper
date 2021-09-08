import requests
import re
import os

headers = {'content-type': 'application/json', 'user-agent': 'Mozilla/5.0'}

def get_leagues(POESESSID=None):
    if POESESSID is not None:
        headers["Cookie"] = "POESESSID=" + POESESSID
        # Gets all current leagues
        all_leagues = requests.get("https://api.pathofexile.com/league?type=main",
                                   headers = headers)
        # Check for if api request fails b/c POESESSID is not valid
        if all_leagues.status_code == 401:
            print("Error 401: POESESSID not valid.")
            return None
        else:
            all_leagues = all_leagues.json()['leagues']
            all_leagues = [league['id'] for league in all_leagues]
        # Gets all private leagues ie. events/voided leagues
        private_leagues = requests.get("https://api.pathofexile.com/league?type=event",
                                   headers = headers).json()['leagues']
        private_leagues = [league['id'] for league in private_leagues]

        # Get only official leagues (standard, hardcore, league standard, league hardcore)
        official_leagues = [league for league in all_leagues if league not in private_leagues]
        official_leagues = [league for league in official_leagues if not(re.match("^SSF.*", league))]
        return official_leagues
    else:
        print("Error: No POESESSID entered. Please enter your POESESSID.")
        return None


def retrieve_id():
    # Get POESESSID if saved, else return none
    if os.path.isfile("poeid.txt"):
        POESESSID = open("poeid.txt", "r").read()
        return POESESSID
    else:
        return None


def choose_league():
    POESESSID = retrieve_id()

    # If preexisting ID does not exist
    if POESESSID is None:
        while True:
            POESESSID = input("Please enter your POESESSID:         ")
            available_leagues = get_leagues(POESESSID=POESESSID)
            if available_leagues != None:
                # Save working ID
                id_file = open("poeid.txt", "w")
                id_file.write(POESESSID)
                break
    # Preexisting ID found
    else:
        available_leagues = get_leagues(POESESSID=POESESSID)
        # If ID doesn't work than manually enter ID
        if available_leagues == None:
            while True:
                POESESSID = input("Please enter your POESESSID:         ")
                available_leagues = get_leagues(POESESSID=POESESSID)
                if available_leagues != None:
                    id_file = open("poeid.txt", "w")
                    id_file.write(POESESSID)
                    break

    print("Choose a league:")
    for index, league in enumerate(available_leagues):
        print("{index}: {league}".format(index=index, league=league))
    while True:
        user_league_choice = input()
        # Checks for if input is correct or not (int between 0 and number of leagues)
        if user_league_choice.isnumeric() and 0 <= int(user_league_choice) and int(user_league_choice) < len(available_leagues):
            user_league_choice = int(user_league_choice)
            print("You have chosen {league}.".format(league=available_leagues[user_league_choice]))
            return available_leagues[user_league_choice]
        else:
            print("Error: Invalid choice.")
