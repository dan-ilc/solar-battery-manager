# postman: https://www.postman.com/collections/c75824e0ea780628bcf3
# https://kb.givenergy.cloud/article.php?id=54

import json
from typing import Tuple
import requests
# from subprocess import Popen

def auth_header():
    return {'Authorization': f'Bearer {NEW_API_KEY}'}
    # return {'Authorization': NEW_API_KEY}
class GivEnergyClient:

    @property

    def _auth_get(self, url: str, body=None):
        return requests.get(url, headers=self.auth_header, json=body)

    def get_mode(self):
        url = f'{BASE_URL}mode'
        return self._auth_get(url)


url = f"{BASE_URL}/communication-device"
print(f"contacting {url}")
resp = requests.get(url, headers=auth_header())
print(resp)
print(resp.json())
