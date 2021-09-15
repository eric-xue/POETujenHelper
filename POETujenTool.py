import keyboard
import pyperclip
import time
import re
import price_retrieval
import league_retrieval_API
import league_retrieval_webscrape
from win32gui import GetWindowText, GetForegroundWindow, SetWindowPos, EnumWindows, GetWindowText
import win32con
import os

# Allow use of colored text
os.system("")

# Setup stay on top toggle
windowList = []
EnumWindows(lambda hwnd, windowList: windowList.append((GetWindowText(hwnd),hwnd)), windowList)
cmdWindow = [i for i in windowList if "POETujenTool.exe" in i[0]]
overlay_alwaysontop = True
if cmdWindow:
    SetWindowPos(cmdWindow[0][1], win32con.HWND_NOTOPMOST, 0, 0, 800, 500, win32con.SWP_NOMOVE)

# Setup dictionaries
clipboard = ""
item_classes = {
    "Stackable Currency" : "Currency",
    "Currency" : "Currency",
    "Map Fragments" : "Fragment"
}
price_index = {
    "Currency" : 1,
    "Fragment" : 2
}

# Initialize prices
while True:
    league_retr_input = input("Choose whether to use your POESESSID or a webscraper to get the current leagues. \n"
                              "[0] POESESSID \n"
                              "[1] Webscraper \n")
    if league_retr_input.isnumeric() and 0 in [0,1]:
        if int(league_retr_input) == 0:
            league = league_retrieval_API.choose_league()
        else:
            league = league_retrieval_webscrape.get_league_scrape()
prices = price_retrieval.init_prices(league)


print("Now waiting for Path of Exile to be selected...")
print("-" * 80)
# Toggled flag to log when POE is focused or not
pathofexile_focused = False
while True:
    if keyboard.is_pressed('ctrl+shift+o') and cmdWindow:
        if overlay_alwaysontop:
            SetWindowPos(cmdWindow[0][1], win32con.HWND_NOTOPMOST, 0, 0, 800, 500,
                         win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            print('\033[91m' + 'Overlay Off' + '\033[0m')
        else:
            SetWindowPos(cmdWindow[0][1], win32con.HWND_TOPMOST, 0, 0, 800, 500,
                         win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            print('\033[92m' + 'Overlay On' + '\033[0m')
        print("-" * 80)
        overlay_alwaysontop = not(overlay_alwaysontop)
        time.sleep(0.1)
        continue
    # Run if POE is in focus
    if GetWindowText(GetForegroundWindow()) == "Path of Exile":
        if not(pathofexile_focused):
            pathofexile_focused = True
            print("Path of Exile detected")
            print("-" * 80)
        while GetWindowText(GetForegroundWindow()) == "Path of Exile":
            # Listen for control+c and extract clipboard when happen
            if keyboard.is_pressed('CTRL+c'):
                # Regex check if copied an item
                # Hacky way to deal with clipboard buffer??????
                try:
                    if re.match("^.*Item Class.*$", pyperclip.paste().splitlines()[0]):
                        clipboard = pyperclip.paste()
                        break
                except Exception:
                    continue
        # Check in case Path of Exile goes out of focus
        if GetWindowText(GetForegroundWindow()) != "Path of Exile":
            continue

        # Extract important info from item description
        item_lines = clipboard.splitlines()
        filtered = [x for x in item_lines if re.match("^.*Item Class.*$|^.*Stack Size.*$",x)]
        filtered.append(item_lines[2])
        # Get type of item
        filtered[0] = item_classes.get(filtered[0].split(': ')[1], "N/A")

        # Preprocess if item is currency to remove max stack amount
        if filtered[0] == "Currency":
            if re.match(".*Stack Size.*", filtered[1]):
                filtered[1] = filtered[1].split(': ')[1].split('/')[0].replace(',' , '')
            else:
                print("Error: {itemname} not supported.".format(itemname=filtered[-1]))
                print("-" * 80)
                # Clears clipboard to fix bug
                pyperclip.copy('')
                time.sleep(0.1)
                continue
        headers = {'content-type': 'application/json'}

        # Calculate total chaos value using stack amount and retrieved price
        # Prices => [Artifact][Currency][Fragment][Oil][Fossil]
        if filtered[0] != "N/A":
            if filtered[0] == "Currency":
                # prices[x][filtered[x]] used to access dictionary, filtered[-1] is name of item
                if re.match(".*Fossil$", filtered[-1]):
                    item_chaos_value = (prices[4][filtered[-1]])*int(filtered[1])
                elif re.match(".*Oil$", filtered[-1]):
                    item_chaos_value = (prices[3][filtered[-1]])*int(filtered[1])
                else:
                    try:
                        item_chaos_value = (prices[1][filtered[-1]])*int(filtered[1])
                    except Exception:
                        print("Error: {itemname} not supported.".format(itemname=filtered[-1]))
                        print("-" * 80)
                        pyperclip.copy('')
                        time.sleep(0.1)
                        continue
            elif filtered[0] == "Fragment":
                item_value = prices[2][filtered[-1]]
                item_chaos_value = int(filtered[1]) * (item_value ** -1)

            # Final calculation of item value in artifacts
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
        # Deal with user holding onto control which seems to copy multiple texts
        pyperclip.copy('')
        time.sleep(0.1)
    # If not in focus, do nothing
    else:
        if (pathofexile_focused):
            pathofexile_focused = False
            print("Path of Exile not detected")
            print("-" * 80)
        time.sleep(0.1)


