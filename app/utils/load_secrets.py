import os
from dotenv import load_dotenv


def load_secrets():
    secrets = {}
    if load_dotenv():
        secrets = {
          'HUGGING_FACE_PASS': os.getenv('HUGGING_FACE_PASS'),
        }
    return secrets
