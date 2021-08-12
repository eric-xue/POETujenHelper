import keyboard
import pyperclip
import time
import re
import requests
import psutil
import init_prices

clipboard = ""
item_classes = {
    "Stackable Currency" : "Currency",
    "Currency" : "Currency",
    "Map Fragments" : "Fragment"
}

prices = init_prices.init_prices()
exit(0)

while True:
    if "PathOfExile.exe" in (p.name()for p in psutil.process_iter()):
        while True:
            time.sleep(0.1)
            if keyboard.is_pressed('CTRL+g'):
                temp = pyperclip.paste()
                if re.match("^.*Item Class.*$", pyperclip.paste().splitlines()[0]):
                    clipboard = pyperclip.paste()
                    break

        item_lines = clipboard.splitlines()
        filtered = [x for x in item_lines if re.match("^.*Item Class.*$|^.*Stack Size.*$",x)]
        filtered.append(item_lines[2])
        print(filtered)

        filtered[0] = item_classes.get(filtered[0].split(': ')[1], "N/A")
        if filtered[0] == "Currency":
            filtered[1] = filtered[1].split(': ')[1].split('/')[0]
        print(filtered[0])
        headers = {'content-type': 'application/json'}
        if filtered[0] != "N/A":
            resp = requests.get("https://poe.ninja/api/data/currencyoverview?",params={"league":"Expedition", "type":filtered[0]}, headers = {'content-type': 'application/json'}).json()
            resp = resp["lines"]
            found_item = None
            for item in resp:
                if item.get('currencyTypeName') == filtered[-1]:
                    print("SAME")
                    found_item = item
                    break
            if found_item is None and filtered[-1] != "Chaos Orb":
                continue

            if filtered[-1] != "Chaos Orb":
                try:
                    item_value = found_item.get('pay').get('value')
                except:
                    break
            else:
                item_value = 1
            if filtered[0] == "Currency":
                item_chaos_value = int(filtered[1])*(item_value**-1)
            else:
                item_chaos_value = (item_value**-1)
            lesser_price = item_chaos_value * prices[0].get("Lesser Black Scythe Artifact")
            common_price = item_chaos_value * prices[0].get("Common Black Scythe Artifact")
            greater_price = item_chaos_value * prices[0].get("Greater Black Scythe Artifact")
            grand_price = item_chaos_value * prices[0].get("Grand Black Scythe Artifact")
            print("Lesser Breakpoint = " + str(lesser_price))
            print("Common Breakpoint = " + str(common_price))
            print("Greater Breakpoint = " + str(greater_price))
            print("Grand Breakpoint = " + str(grand_price))
    else:
       time.sleep(0.5)


