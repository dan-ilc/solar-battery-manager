# postman: https://www.postman.com/collections/c75824e0ea780628bcf3
# https://kb.givenergy.cloud/article.php?id=54

from datetime import timedelta
import json
from typing import Tuple
import requests
# from subprocess import Popen

BASE_URL = "https://api.givenergy.cloud/v1"

def auth_header():
    return {'Authorization': f'Bearer {NEW_API_KEY}'}
class GivEnergyClient:

    def __init__(self):
        data = self.get_battery_data()
        # if data["batteryStatus"] == "WAITING" and data[
        #         "batteryPercent"] == "0" or data["batteryStatus"] is None:
        #     _ = Popen(
        #         ["say", "aaahgghghghghg battery disconnected E C H are morons"])
        #     raise Exception("!!!BATTERY NOT CONNECTED, CHECK TRIP SWITCH!!!")

    def _auth_post(self, url: str, body=None):
        return requests.post(url, headers=auth_header(), json=body)

    def _auth_get(self, url: str, body=None):
        return requests.get(url, headers=auth_header(), json=body)

    def get_mode(self):
        url = f'{BASE_URL}mode'
        return self._auth_get(url)

    def get_presets(self):
        url = f'{BASE_URL}/inverter/{INVERTER_SERIAL}/presets'
        return self._auth_get(url)

    def set_export_times(
        self,
        start_time: str,
        end_time: str,
        second_start_time: str = "",
        second_end_time: str = "",
    ):

        battery_max_power_setting_id = 73
        export_power_w = 3000
        p = self.write_setting(battery_max_power_setting_id, export_power_w)
        print(p.json())
        return self.set_preset(preset_id=3,
                        start_time=start_time,
                        end_time=end_time,
                        second_start_time=second_start_time,
                        second_end_time=second_end_time)

    def set_non_export_times(
        self,
        start_time: str,
        end_time: str,
        second_start_time: str = "",
        second_end_time: str = "",
    ):
        return self.set_preset(preset_id=0,
                        start_time=start_time,
                        end_time=end_time,
                        second_start_time=second_start_time,
                        second_end_time=second_end_time)




    def set_preset(
        self,
        preset_id: int,
        start_time: str,
        end_time: str,
        second_start_time: str = "",
        second_end_time: str = "",
    ):
        # from datetime import datetime, timedelta
        # start_time = (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%SZ')

        # end_time = (datetime.now() + timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f'{BASE_URL}/inverter/{INVERTER_SERIAL}/presets/{preset_id}?start_time={start_time}&end_time={end_time}&enabled=1'
        if second_end_time and second_start_time:
            url = url + f"&second_end_time={second_end_time}&second_start_time={second_start_time}"

        headers = {
            'Authorization': f'Bearer {NEW_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        print(url)
        return requests.post(url, headers=headers)

    def read_setting(self, setting_id:int):
        url = f'{BASE_URL}/inverter/{INVERTER_SERIAL}/settings/{setting_id}/read'
        return self._auth_post(url)

    def write_setting(self, setting_id:int, value:str):
        payload = {
            "value": value
        }
        headers = {
        'Authorization': f'Bearer {NEW_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }
        url = f'{BASE_URL}/inverter/{INVERTER_SERIAL}/settings/{setting_id}/write'
        return requests.post(url, headers=headers, json=payload)





    def set_mode(self, mode: int):
        """
        >>> gc = GivEnergyClient()
        >>> start_mode = gc.get_mode()
        >>> gc.set_mode(2)
        {'success': True}
        >>> gc.get_mode()
        2
        >>> gc.set_mode(start_mode)
        {'success': True}
        >>> assert gc.get_mode() == start_mode
        """
        if mode not in [1, 2, 3, 4]:
            raise ValueError("Mode must be 1-4")
        url = f'{BASE_URL}mode'
        return self._auth_post(url, {"mode": str(mode)})

    def schedule_discharge(self, start_time: int, end_time: int,
                           target_pc: int):
        """
        >>> gc = GivEnergyClient()
        >>> gc.schedule_discharge(1000,1100,5)
        ...
        >>> gc.get_discharge_interval()
        ('1000', '1100')
        """
        assert start_time > 0 and start_time <= 2359
        assert end_time > 0 and end_time <= 2359
        assert start_time < end_time
        assert target_pc >= 4 and target_pc < 100

        body = {
            "enable": "true",
            "start": str(start_time),
            "finish": str(end_time),
            "dischargeToPercent": str(target_pc)
        }
        url = f'{BASE_URL}dischargeBattery'
        return self._auth_post(url, body)

    def schedule_charge(self, start_time: int, end_time: int, target_pc: int):
        """
        >>> gc = GivEnergyClient()
        >>> gc.schedule_charge(1000,1100,5)
        ...
        >>> gc.get_charge_interval()
        ('1000', '1100')
        """
        assert start_time > 0 and start_time <= 2359
        assert end_time > 0 and end_time <= 2359
        assert start_time < end_time
        assert target_pc >= 4 and target_pc < 100

        body = {
            "enable": "true",
            "start": str(start_time),
            "finish": str(end_time),
            "chargeToPercent": str(target_pc)
        }
        url = f'{BASE_URL}chargeBattery'
        return self._auth_post(url, body)

    def get_battery_data(self):
        url = f'{BASE_URL}batteryData/all'
        return self._auth_get(url)

    def get_register(self, register_id):
        url = f'{BASE_URL}registers/{register_id}'
        return self._auth_get(url)


    def get_setting(self, setting_id:int):
        url = f'{BASE_URL}settings/{setting_id}/read'
        return self._auth_get(url)

    def set_register(self, register_id: str, value: str):
        url = f'{BASE_URL}registers/{register_id}'
        body = {"value": value}
        return self._auth_post(url, body=body)


    # def set_eco_mode(self):
    #     url = f'{BASE_URL}registers/{register_id}'
    #     body = {"value": value}
    #     return self._auth_post(url, body=body)


    def get_discharge_interval(self) -> Tuple[int, int]:
        data = self.get_battery_data()
        start = data["dischargeScheduleStart"]
        end = data["dischargeScheduleEnd"]
        return (int(start), int(end))

    def get_charge_interval(self) -> Tuple[int, int]:
        data = self.get_battery_data()
        start = data["chargeScheduleStart"]
        end = data["chargeScheduleEnd"]
        return (int(start), int(end))

    def cancel_discharge(self):
        # cancels all the discharging for today
        body = {
            "enable": "false",
            "start": "0000",
            "finish": "0001",
            "chargeToPercent": "5"
        }
        url = f'{BASE_URL}dischargeBattery'
        return self._auth_post(url, body)

    def cancel_charge(self):
        # cancels all the charge from today
        body = {
            "enable": "false",
            "start": "0000",
            "finish": "0001",
            "chargeToPercent": "5"
        }
        url = f'{BASE_URL}chargeBattery'
        return self._auth_post(url, body)


def main():
    gc = GivEnergyClient()
    # p = gc.get_presets()
    # print(p.json())
    # p = gc.set_preset(2, "16:30", "19:00")
    # p= gc.read_setting("73")
    # print(p.json())
    # p= gc.write_setting("73", 1000)
    # print(p.json())
    # print(gc.read_setting("73").json())

    p = gc.set_export_times("16:30", "19:00")
    print(p.json())
    p = gc.set_non_export_times("19:00", "23:59", "00:00","16:30")
    print(p.json())


    # print(p.status_code)
    # try:
    #     print(p.json())
    # except:
    #     print(p.content)


    # register_ids = [
    #     "selfConsumption",
    #     "chargeFlag",
    #     "chargeStart",
    #     "chargeEnd",
    #     "dischargeFlag",
    #     "dischargeStart",
    #     "dischargeEnd",
    #     "shallowValue",
    #     "chargeUpTo",
    #     "dischargeDownTo",
    #     "chargeRate",
    #     "dischargeRate",
    # ]
    # # print(gc.get_register("dischargeRate"))
    # # print(gc.get_register("dischargeStart"))
    # # # print(gc.set_register("dischargeStart", "1730"))
    # # print(gc.set_register("dischargeEnd", "700"))
    # print(gc.get_register("dischargeEnd"))
    # print(gc.get_register("dischargeStart"))
    # print(gc.get_register("dischargeEnd"))

    # print('dischargedownto')
    # print(gc.get_register("dischargeDownTo"))
    # # print(gc.set_register("dischargeDownTo", "3"))
    # print(gc.get_register("dischargeDownTo"))
    # print("Shallowvalue")
    # print(gc.get_register("shallowValue"))
    # # print(gc.set_register("shallowValue", "3"))
    # print(gc.get_register("shallowValue"))
    # print('register_id,register_value')
    # for register_id in register_ids:
    #     value = gc.get_register(register_id)
    #     print(f"{register_id},{value}")


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    main()
