import os, requests, uuid, json
from dotenv import load_dotenv

load_dotenv()

def get_translation(reference, selectedLanguage, resultLanguage):
  
  key = os.environ.get("TRANSLATOR_TEXT_SUBSCRIPTION_KEY")
  endpoint = os.environ.get("TRANSLATOR_TEXT_ENDPOINT")
  location = os.environ.get("TRANSLATOR_TEXT_REGION")
  
  path = "/translate?api-version=3.0"
  params = f"&from={selectedLanguage}&to={resultLanguage}"
  constructed_url = endpoint + path + params
  
  headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Ocp-Apim-Subscription-Region": location,
    "Content-type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4())
  }
  
  body = [{
    "text" : reference 
  },]
  
  request = requests.post(
    constructed_url,
    headers = headers,
    json = body
  )

  response = request.json()
  
  print(f"translation: {response[0]["translations"][0]["text"]}")  
  return response[0]["translations"][0]["text"] 
