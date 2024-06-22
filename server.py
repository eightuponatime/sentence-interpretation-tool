import candidate
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
import os
import detection
import translation
import spell_check

app = Flask(__name__)
load_dotenv()

CORS(app,origins="https://amd64react-frontend-r5vrjzoy5a-uc.a.run.app",
  allow_headers=["Content-Type","Authorization"],
  methods=["GET","POST","PUT","DELETE","OPTIONS"],
  supports_credentials=True
)

api_key = os.environ.get("AZURE_OPENAI_API_KEY")
endpoint = os.environ.get("AZURE_OPENAI_API_ENDPOINT")
deployment = os.environ.get("DEPLOYMENT") 
  
# [API] formatting the entered text
@app.route("/get_reference", methods = ["POST"], strict_slashes = False)
def get_reference():
   
  client = AsyncAzureOpenAI(
    api_key = api_key,
    api_version = "2024-02-01",
    azure_endpoint = endpoint 
  )
  
  reference = request.json['reference']
  selectedLanguage = detection.get_language(reference)
  resultLanguage = request.json['resultLanguage']

  match resultLanguage:
    case "Russian":
      resultLanguage = "ru"
    case "Kazakh":
      resultLanguage = "kk"
    case "English":
      resultLanguage = "en"
  
  translated_reference = ""
  corrected_reference = ""
   
  if resultLanguage == selectedLanguage:
    result = candidate.get_highest_score(reference, client, resultLanguage)   
  else:
    match selectedLanguage:
      case "ru":
        corrected_reference = spell_check.spell_check(reference, selectedLanguage)
      case "en":
        corrected_reference = spell_check.spell_check(reference, selectedLanguage)
      case "kk":
        corrected_reference = spell_check.kazakh_spell_check(reference)
    
    translated_reference = translation.get_translation(
      reference = corrected_reference,
      selectedLanguage = selectedLanguage,
      resultLanguage = resultLanguage
    )
    
    result = candidate.get_highest_score(translated_reference, client, resultLanguage) 
 
  return jsonify({
    "result": result["result"],
    "results": result["results"],
    "translated_reference": translated_reference
  })

# [API] detect the input language
@app.route("/detect_language", methods = ["POST"], strict_slashes = False)
def detect_language():
  
  reference = request.json['reference']
  language = detection.get_language(reference)  

  match language:
    case 'ru':
      language = "Russian"
    case 'kk':
      language = "Kazakhзадание"
    case 'en':
      language = "English"
  
  print(f"detected language is {language}")
  return jsonify({ "language": language })
  
# start server
if __name__ == '__main__':
  #app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 8000)), debug=True)
  app.run(port=int(os.environ.get("PORT", 8000)))
