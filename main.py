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

price_index = {
    "Currency" : 1,
    "Fragment" : 2
}

while True:
    if "PathOfExile.exe" in (p.name()for p in psutil.process_iter()):
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

        filtered[0] = item_classes.get(filtered[0].split(': ')[1], "N/A")
        if filtered[0] == "Currency":
            filtered[1] = filtered[1].split(': ')[1].split('/')[0]
        headers = {'content-type': 'application/json'}
        if filtered[0] != "N/A":
            if filtered[0] == "Currency":
                if re.match(".*Fossil$", filtered[-1]):
                    item_chaos_value = (prices[4][filtered[-1]])*int(filtered[1])
                elif re.match(".*Oil$", filtered[-1]):
                    item_chaos_value = (prices[3][filtered[-1]])*int(filtered[1])
                else:
                    item_chaos_value = (prices[1][filtered[-1]])*int(filtered[1])
            elif filtered[0] == "Fragment":
                item_value = prices[2][filtered[-1]]
                item_chaos_value = int(filtered[1]) * (item_value ** -1)
            lesser_price = item_chaos_value * prices[0].get("Lesser Black Scythe Artifact")
            common_price = item_chaos_value * prices[0].get("Common Black Scythe Artifact")
            greater_price = item_chaos_value * prices[0].get("Greater Black Scythe Artifact")
            grand_price = item_chaos_value * prices[0].get("Grand Black Scythe Artifact")
            print(filtered)
            print("Lesser Breakpoint = " + str(lesser_price))
            print("Common Breakpoint = " + str(common_price))
            print("Greater Breakpoint = " + str(greater_price))
            print("Grand Breakpoint = " + str(grand_price))
        else:
            print("Error: Item copied could not be found.")
            print(item_lines)
    else:
       time.sleep(0.5)


