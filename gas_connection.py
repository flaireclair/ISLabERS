import requests
import json
from config.config import *

class GASConnection():
    def postData(self, data):
        if(data is None):
            print("params is empty")
            return False
        
        payload = {
            "data": data
        }
        url = GAS_APP_URL
        headers = {
            'Content-Type': 'application/json',
        }
        jdata = json.dumps(payload)
        response = requests.post(url, data=jdata, headers=headers)
        # print(jdata)
        if(response.status_code == 200 and response.text == "success"):
            if(data["event"] == "ENTER"):
                print("おはようございます。")
            else:
                print("お疲れ様でした。")
            return True
        print(response.text)
        return False
