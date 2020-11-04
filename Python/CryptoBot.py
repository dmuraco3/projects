try:
    import requests
except ModuleNotFoundError:
    modules_not_installed = []

import requests
import os
import subprocess
from decouple import config
import json
from time import sleep
import math
from termcolor import colored
import numpy
from datetime import datetime

file_exists = os.path.exists(".env")

if file_exists == False:
    print("If you already have NOMICS api key please input it below")
    print("If you don't have a NOMICS api key please get it here: \n https://p.nomics.com/cryptocurrency-bitcoin-api")

    NOMICS_API_KEY = input("NOMICS_API_KEY: ")
    NOMICS_API_KEY = str(NOMICS_API_KEY)

    with open(".env", "w") as f:
        f.write("NOMICS_API_KEY=" + NOMICS_API_KEY)
    print("done")

if file_exists == True:
    NOMICS_API_KEY = config('NOMICS_API_KEY')

dictionary = dict()

history = []
historical_EMA10 = []
historical_EMA20 = []
historical_EMA50 = []


L50 = list(range(1, 51))

i = 0
N10 = 10
N20 = 20
N50 = 50

position = "NaN"

def get_previous_price():
    if i > 0:
        global previous_price
        previous_price = current_price
        return previous_price

    

def get_current_price():
    global current_price
    
    try:
        response = requests.get("https://api.nomics.com/v1/currencies/ticker?key=" + NOMICS_API_KEY + "&ids=BTC&interval=1h")
        json = response.json()
        current_price = float(json[0]['price'])
    except Exception:
        print("could not get data, RETRYING...")

    if i > 0:
        if current_price > previous_price:
            print(colored("Current BTC Price:", "white"), colored(current_price, "green"))
        elif current_price < previous_price:
            print(colored("Current BTC Price:", "white"), colored(current_price, "red"))
        elif current_price == previous_price:
            print(colored("Current BTC Price:", "white"), colored(current_price, "white"))
    else:
        print("Current BTC Price:", current_price)
    return current_price
 
def point_10_average():
    global result10
    global SMA10
    global EMA10
    global previous_EMA10
    if len(history) == N10:
        result10 = history[-N10:]
        SMA10 = (sum(result10)) / N10
        EMA10 = current_price * (2 / (N10 + 1)) + SMA10 * (1 - (2 / (N10 + 1)))
        print("EMA10:", EMA10)
        return EMA10
    elif len(history) > N10:
        previous_EMA10 = EMA10
        EMA10 = current_price * (2 / (N10 + 1)) + previous_EMA10 * (1 - (2 / (N10 + 1)))
        print("previous EMA10:", previous_EMA10)
        print("EMA10:", EMA10)
        return EMA10, previous_EMA10

def point_20_average():
    global result20
    global SMA20
    global EMA20
    global previous_EMA20
    if len(history) == N20:
        result20 = history[-N20:]
        SMA20 = (sum(result20)) / N20
        EMA20 = current_price * (2 / (N20 + 1)) + SMA20 * (1 - (2 / (N20 + 1)))
        print("EMA20:", EMA20)
        return EMA20
    elif len(history) > N20:
        previous_EMA20 = EMA20
        EMA20 = current_price * (2 / (N20 + 1)) + previous_EMA20 * (1 - (2 / (N20 + 1)))
        print("previous EMA20:", previous_EMA20)
        print("EMA20:", EMA20)
        return EMA20, previous_EMA20

def point_50_average():
    global result50
    global SMA50
    global EMA50
    global previous_EMA50
    if len(history) == N50:
        result50 = history[-N50:]
        SMA50 = (sum(result50)) / N50
        EMA50 = current_price * (2 / (N50 + 1)) + SMA50 * (1 - (2 / (N50 + 1)))
        print("EMA50:", EMA50)
        return EMA50
    elif len(history) > N50:
        previous_EMA50 = EMA50
        EMA50 = current_price * (2 / (N50 + 1)) + previous_EMA50 * (1 - (2 / (N50 + 1)))
        print("previous EMA50:", previous_EMA50)
        print("EMA50:", EMA50)
        return EMA50, previous_EMA50

def store_data():
    dictionary[dt_string] = {}
    dictionary[dt_string]["price"] = current_price
    if len(history) > N10:
        dictionary[dt_string]["EMA10"] = EMA10
    if len(history) > N20:
        dictionary[dt_string]["EMA20"] = EMA20
    if len(history) > N50:
        dictionary[dt_string]["EMA50"] = EMA50
    
    if i % 50==0:
        with open('data.json', 'w') as fp:
            json.dump(dictionary, fp, sort_keys=True, indent=4)
    
    return dictionary, dictionary[dt_string]



while True:
    sleep(10)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if len(history) > 1:
        store_data()
    get_previous_price()
    get_current_price()
    i +=1 
    
    if len(history) >= N10:
        point_10_average()
    if len(history) >= N20:
        point_20_average()
    if len(history) >= 50:
        point_50_average()

    if len(history) >= (N50 + 5):
        if position == "NaN":
            if EMA10 > EMA20 and EMA10 > EMA50:
                print(colored("bought 1 BTC at " + str(current_price), "magenta"))
                position = "bought"
                buy_price = current_price
        elif position == "sold":
            if EMA10 > EMA20 and EMA10 > EMA50:
                print(colored("bought 1 BTC at " + str(current_price), "magenta"))
                position = "bought"
                buy_price = current_price
        if position == "bought":
            if EMA10 < EMA20:
                sell_price = current_price
                total = sell_price - buy_price
                x = sell_price > buy_price
                print(colored("sold 1 BTC at a profit of " + str(total), "magenta"))
                position = "sold"

    history.append(current_price)
    
    if len(history) > N10:
        historical_EMA10.append(EMA10)
            
    if len(history) > N20:
        historical_EMA20.append(EMA20)
    
    if len(history) > N50:
        historical_EMA50.append(EMA50)