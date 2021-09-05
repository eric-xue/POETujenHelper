import keyboard
import pyperclip
import time
import re
import requests
import psutil
import init_prices
from win32gui import GetWindowText, GetForegroundWindow

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

pathofexile_focused = False
while True:
    if GetWindowText(GetForegroundWindow()) == "Path of Exile":
        if not(pathofexile_focused):
            pathofexile_focused = True
            print("Path of Exile detected")
            print("-" * 80)
        while GetWindowText(GetForegroundWindow()) == "Path of Exile":
            time.sleep(0.1)
            if keyboard.is_pressed('CTRL+c'):
                temp = pyperclip.paste()
                if re.match("^.*Item Class.*$", pyperclip.paste().splitlines()[0]):
                    clipboard = pyperclip.paste()
                    break
        if GetWindowText(GetForegroundWindow()) != "Path of Exile":
            continue

        item_lines = clipboard.splitlines()
        filtered = [x for x in item_lines if re.match("^.*Item Class.*$|^.*Stack Size.*$",x)]
        filtered.append(item_lines[2])

        filtered[0] = item_classes.get(filtered[0].split(': ')[1], "N/A")
        if filtered[0] == "Currency":
            if re.match(".*Stack Size.*", filtered[1]):
                filtered[1] = filtered[1].split(': ')[1].split('/')[0].replace(',' , '')
            else:
                print("Error: {itemname} not supported.".format(itemname=filtered[-1]))
                print("-" * 80)
                continue
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

            print("Item: {item} \n"
                  "Amount: {stacksize} \n"
                  "Total Chaos Value: {chaosvalue} \n\n"
                  "Lesser Artifact Breakpoint = {lesser_price} \n"
                  "Common Artifact Breakpoint = {common_price} \n"
                  "Greater Artifact Breakpoint = {greater_price} \n"
                  "Grand Artifact Breakpoint = {grand_price}"
                  .format(item=filtered[2], stacksize=filtered[1], chaosvalue=item_chaos_value, lesser_price=lesser_price,
                          common_price=common_price,greater_price=greater_price,grand_price=grand_price))
        else:
            print("Error: Item copied could not be found.")
            print(item_lines)
        print("-" * 80)
    else:
        if (pathofexile_focused):
            pathofexile_focused = False
            print("Path of Exile not detected")
            print("-" * 80)
        time.sleep(0.5)


