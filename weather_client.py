# importing requests and json
import requests, json
from datetime import datetime

base_url = "https://api.solcast.com.au/rooftop_sites/"
west_id = "6b57-78ef-7c0f-d7c2"
east_id = "28fc-39cf-d1ab-6720"
api_key = "5OoV1_9qtwrgXAclpE7P4WG-nUIcMRwz"
period_length_hours = 0.5  # PT30M is default for forecast endpoint



def from_str(time_str: str) -> datetime:
   TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%f0Z'
   return datetime.strptime(time_str, TIMESTAMP_FORMAT)


def is_tomorrow(time: datetime):
    today = datetime.now().day
    return time.day == today + 1


def get_forecast_from_site(site_id: str):
    forecast_url = f"{base_url}/{site_id}/forecasts?format=json&api_key={api_key}"
    forecast_raw = requests.get(forecast_url).json()

    tomorrow_total_kwh = 0
    for forecast in forecast_raw["forecasts"]:
        period_end = from_str(forecast["period_end"])
        # print(period_end)
        if is_tomorrow(period_end):
            energy_kwh = forecast["pv_estimate"] * period_length_hours
            # print(f"adding {energy_kwh}kWh of energy")
            tomorrow_total_kwh += energy_kwh
    return tomorrow_total_kwh


def estimate_tomorrow_solar():
    tomorrow_solar_gen_kwh = get_forecast_from_site(
        west_id) + get_forecast_from_site(east_id)
    return tomorrow_solar_gen_kwh

def estimate_tomorrow_consumption_kwh()->float:
   if datetime.now().weekday() >= 5: # weekend
      return 6.0
   else:
      return 10.0


def main():
   tomorrow_solar_gen_kwh = estimate_tomorrow_solar()
   print(f"we will generate {tomorrow_solar_gen_kwh} kWh tomorrow.")
   tomorrow_consumption = estimate_tomorrow_consumption_kwh()
   print(f"we will use {tomorrow_consumption} kWh tomorrow.")
   tomorrow_net_change = tomorrow_solar_gen_kwh - tomorrow_consumption
   print(f"net change: {tomorrow_net_change} kWh.")
   pc = tomorrow_net_change*100/8.2
   print(f"net change: {pc} %.")

main()
