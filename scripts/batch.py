from urllib.request import Request

import schedule as schedule
import requests
import json
import asyncio
import datetime
from os import environ
from dotenv import load_dotenv

load_dotenv()


# 5분마다 기초데이터 채우기 로직
async def reset():
    url = environ["BATCH_URL"]

    payload = json.dumps({
    })
    headers = {
        'Content-Type': 'application/json'
    }

    print("기초 데이터 리셋")

    response = requests.request("POST", url, headers=headers, data=payload)
    result = json.loads(response.text)["result"]

    if result != 0:
        print("기초 데이터 채우기 실패")

    await asyncio.sleep(60 * 10)
    # * 5)


while True:
    asyncio.run(reset())
