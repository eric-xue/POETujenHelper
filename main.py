import keyboard
import pyperclip
import time
import re
import requests

clipboard = ""
item_classes = {
    "Stackable Currency" : "Currency",
    "Currency" : "Currency",
    "Map Fragments" : "Fragment"
}
while True:
    while True:
        time.sleep(0.1)
        if keyboard.is_pressed('CTRL+c'):
            temp = pyperclip.paste()
            if re.match("^.*Item Class.*$", pyperclip.paste().splitlines()[0]):
                clipboard = pyperclip.paste()
                break

    item_lines = clipboard.splitlines()
    filtered = [x for x in item_lines if re.match("^.*Item Class.*$|^.*Stack Size.*$",x)]
    filtered.append(item_lines[2])
    print(filtered)

    filtered[0] = item_classes.get(filtered[0].split(': ')[1], "N/A")
    print(filtered[0])
    headers = {'content-type': 'application/json'}
    if filtered[0] != "N/A":
        resp = requests.get("https://poe.ninja/api/data/currencyoverview?",params={"league":"Expedition", "type":filtered[0]}, headers = {'content-type': 'application/json'}).json()
        resp = resp["lines"]
        for item in resp:
            if item.get('currencyTypeName') == filtered[-1]:
                print("SAME")
        print(resp)

#
# Item Class: Map Fragments
# Rarity: Normal
# Esh's Breachstone
# --------
# Travel to Esh's Domain by using this item in a personal Map Device. Can only be used once.
