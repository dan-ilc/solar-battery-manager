# postman: https://www.postman.com/collections/c75824e0ea780628bcf3
# https://kb.givenergy.cloud/article.php?id=54

import json
from typing import Tuple
import requests
# from subprocess import Popen

BATTERY_API_KEY = "aw7RtfwDr1SQLmleofh8EoHZmEd9FG"
INVERTER_SERIAL = "CE2122G224"
GIV_USERNAME = "danmangles"
GIV_API_KEY = "79f77b0483657b9da93cc023db4b53f10bdf3517901db01e051adb0eb48a1c5e647c150e7cfca85145cb1b8e2604ea1d"

BASE_URL = "https://api.givenergy.cloud/v1"
NEW_API_KEY="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NTc3MDIxOS1jYWE2LTRmOTctOTE3Ni0zNDBlZGMzZDQxNTgiLCJqdGkiOiJkNjlmYTMxYjFjNTk0Nzg2MzU1YjIyZTk3OTNmNmVjNjI5YWVjMGM5OWJkZDVlMTc2ZjY5ZDgwNjY3MDc0N2FiZDRjODVmZDk5NWE0YjhjNCIsImlhdCI6MTY0ODMxMzcwOS4xNTAxMTgsIm5iZiI6MTY0ODMxMzcwOS4xNTAxMjIsImV4cCI6MTY3OTg0OTcwOS4xNDIwOTcsInN1YiI6IjU4NTIiLCJzY29wZXMiOlsiYXBpIl19.HLi2fhRng5h5scOQEr8_c4HEcUirYEhK7e-XupSSd2o5vA5iS72TK8IlEk5pRlrsfKZL9emesKHzhBloECXeCTz4UN6Jw4J30yiTyIlf094W31CIT9Vak6teQDoGfUIP7ARoZj4sQbQerID-fUXlQ2ESNC2bpmdk4EpLNdecAj-t3Bs5bvs4YvYRruKO13Qt6NMEdyCDWsrB9JotP2kbAADCLrMhx3Rd6AwBLhx-jXDBmMSil-4uJvH1OiOr3c58vm3V_6-Idf0lV9_CcHQWkDBkEePo_yYhmJi0Vlm3E39jSXHmUDDBsUgm-FgqU92LRTEyaFDZcnkoY8ard6YV9aXZUy0DywPmYekaimSPT6K16_4zOVE8n1UDd8Ritu0NjCErLpsbA8hYWjuPO9Macmayyy86cB6sctixFH8qi2fb_4cghPM9nNcpGY69vOpgwF0Z57XyF4mQxqMM4a1hByX9IfVEEbsSI9_H1qFDR6sN54eJjoNbLms3mHKxZ5qiIPP6VyfXZHqDKWpoyDWiOTpIERBTZCvyPEKOlKLJOTsyZu29XtM-YEJCBdSf9UEHQq6KJw6uQvDCLQQccUgPfVz5uGsnV5nnOI20sZqCVDBO3PUjtYXvg2utCrinJ29tGl7Q_Hv424nM2XXm1KJGR3kCoTjJve4nR0Ba0_6mmAw"

def auth_header():
    return {'Authorization': f'Bearer {NEW_API_KEY}'}
    # return {'Authorization': NEW_API_KEY}
class GivEnergyClient:
    api_key = "aw7RtfwDr1SQLmleofh8EoHZmEd9FG"

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
