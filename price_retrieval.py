import requests
import re
import datetime

def init_prices(league):
    # Init storage
    artifact_prices = {}
    currency_prices = {}
    frag_prices = {}
    oil_price = {}
    fossil_price = {}
    aggregate_prices = []

    print("Initializing prices...")
    # Get artifact prices
    tujen_currency = "Black Scythe Artifact"
    resp = requests.get("https://poe.ninja/api/data/ItemOverview?",params={"league":league, "type":"Artifact"}, headers = {'content-type': 'application/json'}).json()["lines"]
    for artifact in resp:
        if re.match("^.*Black Scythe Artifact.*$", artifact["name"]):
            artifact_prices[artifact["name"]] = (artifact["chaosValue"]**-1)
    aggregate_prices.append(artifact_prices)
    # Get currency prices
    resp = requests.get("https://poe.ninja/api/data/currencyoverview?",params={"league":league, "type":"Currency"}, headers = {'content-type': 'application/json'}).json()["lines"]
    for entry in resp:
        currency_prices[entry["currencyTypeName"]] = entry["chaosEquivalent"]
    currency_prices["Chaos orb"] = 1
    aggregate_prices.append(currency_prices)
    # Get fragment prices
    resp = requests.get("https://poe.ninja/api/data/currencyoverview?",params={"league":league, "type":"Fragment"}, headers = {'content-type': 'application/json'}).json()["lines"]
    for entry in resp:
        frag_prices[entry["currencyTypeName"]] = entry["chaosEquivalent"]
    aggregate_prices.append(frag_prices)
    # Get oil prices
    resp = requests.get("https://poe.ninja/api/data/ItemOverview?",params={"league":league, "type":"Oil"}, headers = {'content-type': 'application/json'}).json()["lines"]
    for entry in resp:
        oil_price[entry["name"]] = entry["chaosValue"]
    aggregate_prices.append(oil_price)
    # Get fossil prices
    resp = requests.get("https://poe.ninja/api/data/ItemOverview?", params={"league": league, "type": "Fossil"}, headers={'content-type': 'application/json'}).json()["lines"]
    for entry in resp:
        fossil_price[entry["name"]] = entry["chaosValue"]
    aggregate_prices.append(fossil_price)

    date_stamp = datetime.datetime.now()
    aggregate_prices.append(date_stamp)

    print("Prices initialized at " + str(date_stamp))

    return aggregate_prices
