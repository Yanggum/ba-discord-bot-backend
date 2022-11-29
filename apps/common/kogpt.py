# coding=utf8
# REST API 호출에 필요한 라이브러리
import requests
from konlpy.tag import Okt
from torch import no_grad
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import openai
from os import environ
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Okt 객체 생성
okt = Okt()


# KoGPT API 호출을 위한 메서드 선언
# 각 파라미터 기본값으로 설정
def kogpt_api(prompt, max_tokens=32):
    url = environ["KOGPT_URL"]
    tokenized = okt.pos(prompt)

    payload = {
        'text': prompt,
        'length': int(len(tokenized) * 1.5) + max_tokens
    }
    files = [
    ]
    headers = {
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response.text


def polyglot_ko_api(prompt, max_tokens=32):
    url = environ["POLYGLOT_URL"]
    headers = {"Authorization": "Bearer " + environ["HUGGINGFACE_AUTH"]}

    def query(payload):
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": prompt,
    })

    try:
        return output[0]["generated_text"]

    except:
        return run_kogpt(prompt, max_tokens)


def run_gpt3(prompt, max_tokens):
    openai.api_key = environ["OPENAI_API_KEY"]

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    return response.choices[0].text


# 파라미터를 전달해 kogpt_api()메서드 호출
def run_kogpt(prompt, max_tokens):
    response = kogpt_api(
        prompt=prompt,
        max_tokens=max_tokens,
    )

    return response
