import requests
from utils.load_secrets import load_secrets

API_URL = "https://api-inference.huggingface.co/models/sismetanin/xlm_roberta_large-ru-sentiment-rusentiment"
token = load_secrets()['HUGGING_FACE_PASS']
headers = {"Authorization": token}


def bert_query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    sentence = response.json()[0]

    return sentence[0]['label'], sentence[0]['score']
