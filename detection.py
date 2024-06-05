from lingua import Language, LanguageDetectorBuilder
import os, requests, uuid, json
from dotenv import load_dotenv

load_dotenv()

def get_language(reference):
  key = os.environ.get("TRANSLATOR_TEXT_SUBSCRIPTION_KEY")
  endpoint = os.environ.get("TRANSLATOR_TEXT_ENDPOINT")
  location = os.environ.get("TRANSLATOR_TEXT_REGION")
  
  path = '/detect?api-version=3.0'
  constructed_url = endpoint + path

  headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
  }

  body = [{
    'text': reference 
  }]
  request = requests.post(constructed_url, headers=headers, json=body)
  response = request.json()

  return response[0]['language']
