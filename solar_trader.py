from datetime import datetime
from numpy import sort
from pyrsistent import get_in
from pytest import param
import requests
from typing import List, Tuple

from octopus_client import OctopusClient
from givenergy_client import GivEnergyClient
from subprocess import Popen


# print(oc.get_export_prices())


# print(gc.get_battery_data())

# Rule 1: Set to sell for any time where the export price is significantly
#         above the import price

# export_prices_24h = oc.get_export_prices()
# import_prices_24h = oc.get_import_rates()

# prods = oc.get_products()
# # print(prods)
# for prod in prods["results"]:
#     # print(prod)
#     if prod["direction"] == "IMPORT" and prod["brand"] == "OCTOPUS_ENERGY":
#         # print(prod)

#         print(prod["code"])
#         print(prod["display_name"])
#         if "TRACKER" in prod["display_name"].upper():
#             break

# print(oc.get_account_details())

def get_times_over_(threshold:float, price_data:list):
    # return a list of times where the unit rate exc vat exceeds threshold

    times_over_thresh = []
    for rate in price_data:
        if rate["value_exc_vat"] > threshold:
            print('got interval over sell thresh')
            times_over_thresh.append(rate)
        # print()
        # print(u)
    # print(times_over_thresh)

    return times_over_thresh

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
def from_str(time_str:str)->datetime:
    return datetime.strptime(time_str,TIMESTAMP_FORMAT)

def get_interval_from_times_list(times)->list:
    if not times:
        return []
    sorted_times = sorted(times, key=lambda x: x["valid_from"])
    print(sorted_times)

    interval_start = sorted_times[0]["valid_from"]
    prev_time = None
    intervals = []
    for time in sorted_times:
        if prev_time:
            if prev_time["valid_to"] == time["valid_from"]:
                print("extending")
            else:
                intervals.append((from_str(interval_start),from_str(prev_time["valid_to"])))
                interval_start = time["valid_from"]
        prev_time = time
    # catch the last interval
    intervals.append((from_str(interval_start), from_str(prev_time["valid_to"])))
    return intervals


def to_hhmm(dt:datetime)->int:
    return dt.hour*100+dt.minute


def get_todays_discharge_interval(threshold:float, price_data: list) -> Tuple[int, int]:
    times = get_times_over_(threshold, price_data)
    if times:
        intervals = get_interval_from_times_list(times)
        print(intervals)
        for interval in intervals:
            print("interval")
            print(interval)
            if interval[0].day == datetime.now().day:
                return (to_hhmm(interval[0]), to_hhmm(interval[1]))

    return None


from time import sleep
def say(text:str):
    print(text)
    # _ = Popen(["say", text])
    # sleep(len(text)*0.1)


# def max_price(price_data:list) -> float:
#     python sor
#     max_price = sort(price_data, key=lambda x: x["value_exc_vat"])
#     print(max_price)
#     assert False
    # return max_price["value_exc_vat"], max_price["valid_from"]

def filter_to_today(price_data:list) -> list:
    filtered_data = []

    for datum in price_data:
        today = datetime.now().day
        if from_str(datum["valid_from"]).day == today:
            filtered_data.append(datum)
    return filtered_data

def filter_to_future(price_data:list) -> list:
    filtered_data = []

    for datum in price_data:
        today = datetime.now().day
        if from_str(datum["valid_from"]) > datetime.now():
            filtered_data.append(datum)
    return filtered_data

def get_percentage(battery_data:dict)->int:
    return int(battery_data["batteryPercent"])


def set_cron():


from subprocess import Popen
def main():
    say("Good afternoon! Let me get your battery client setup.")
    gc = GivEnergyClient()

    status = gc.get_battery_data()
    pc = get_percentage(status)
    say(f"All set. Battery at {pc}%")
    print(status)

    say("And now i'll set up the octopus client")
    oc = OctopusClient()
    sell_thresh = 30  #p/kwh
    charge_thresh = sell_thresh + 20  #p/kwh
    say("\n\nGetting export prices...")
    export_prices = oc.get_export_prices()["results"]
    export_prices_future = filter_to_future(export_prices)
    print(export_prices_future)
    # todo: get the best 5 prices

    max, maxtime= max_price(export_prices_today)
    # max_time_dt:datetime= from_str(maxtime)
    say(f"Got prices. Max price: {max}p/kWh at {max_time_dt.hour}:{max_time_dt.minute}")
    print("\nSetting discharge interval")
    today_interval = get_todays_discharge_interval(sell_thresh, export_prices_today)
    if not today_interval:
        say(
            f"There are no times today where the export price exceeds {sell_thresh}p/kWh. Planning normal discharge."
        )
        # gc.schedule_discharge(1, 2359, 4)
        # gc.cancel_discharge()
    else:
        say(f"\nScheduling a discharge from {today_interval[0]} to {today_interval[1]}")
        # gc.schedule_discharge(today_interval[0], today_interval[1], 5)

    print(gc.get_battery_data())
# Rule 2: If the export price will spike significantly above the import price,
#         charge by the max amount we could sell at that price, provided it
#         the battery will not fill as a result
main()
