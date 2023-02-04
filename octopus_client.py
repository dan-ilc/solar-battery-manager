from datetime import datetime
from numpy import sort
from pyrsistent import get_in
from pytest import param
import requests
from typing import List, Tuple

from givenergy_client import GivEnergyClient


API_KEY="sk_live_nKwF6l22KbdsePu6YXKbdzTC"
ACCOUNT_NO="A-5ACFDBD4"
EXPORT_MPAN="1411949651009"
IMPORT_MPAN="1470001346836"
IMPORT_SERIAL="16P0348783"
# EXPORT_SERIAL="EML2124552479"
INVERTER_SERIAL="CE2122G224"
EXPORT_SERIAL=IMPORT_SERIAL

#Your gas meter-point’s MPRN is: 2403165205
# Your gas meter’s serial number is: G4P03137891700

# export tarrif is E-1R-AGILE-OUTGOING-19-05-13-E
EXPORT_PRODUCT_CODE="AGILE-OUTGOING-19-05-13"


# def get_all_pages():
#     url = "https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-E/standard-unit-rates/"
#     while url:
#         response = make_request(url) # ['count', 'next', 'previous', 'results']
#         url = response["next"]
#         print(url)
#         print(response["results"][:5])
#     print('done')

class OctopusClient:
    api_key = "sk_live_nKwF6l22KbdsePu6YXKbdzTC"
    def _auth_post(self, url: str, body=None):
        return requests.post(url, auth=(self.api_key,''), json=body).json()

    def _auth_get(self, url: str, body=None):
        return requests.get(url, auth=(self.api_key,''), json=body).json()

    def get_account_details(self):
        url=f'https://api.octopus.energy/v1/accounts/{ACCOUNT_NO}/'
        return self._auth_get(url)

    def get_export_prices(self):
        url = "https://api.octopus.energy/v1/products/AGILE-OUTGOING-19-05-13/electricity-tariffs/E-1R-AGILE-OUTGOING-19-05-13-C/standard-unit-rates/"
        return self._auth_get(url)

    def get_export_amounts(self):
        url=f"https://api.octopus.energy/v1/electricity-meter-points/{EXPORT_MPAN}/meters/{EXPORT_SERIAL}/consumption/"
        r = self._auth_get(url)
        print(r)
        if "404" in str(r):
            raise Exception("got a 404!!!")
        return r

    def get_gas_consumption(self):
        url=f"https://api.octopus.energy/v1/gas-meter-points/2403165205/meters/G4P03137891700/consumption/"
        r = self._auth_get(url)
        print(r)
        if "404" in str(r):
            raise Exception("got a 404!!!")
        return r

    def get_import_rates(self):
        url = "https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-E/standard-unit-rates/"

        return self._auth_get(url)


    def get_products(self):
        url = "https://api.octopus.energy/v1/products"
        return requests.get(url, auth=(self.api_key,''), params={"tarrif_active_at":"2021-08-20T00:00Z"}).json()
        # return self._auth_get(url)

# print(oc.get_account_details())
# products = oc.get_products()["results"]
# for prod in products:
#     # print(prod)
#     if prod["direction"] == "IMPORT":# and prod["brand"] == "OCTOPUS_ENERGY":
#         # print(prod)
#         print()
#         print(prod["display_name"])
#         print(prod["code"])
#         print(prod["links"])
#         if "TRACKER" in prod["display_name"].upper():
#             break
# url = "https://api.octopus.energy/v1/products/SILVER-2017-1/electricity-tariffs/E-1R-SILVER-2017-1-E/day-unit-rates/"
# ############################################################


