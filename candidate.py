import os
import asyncio
import openai
from dotenv import load_dotenv
from sacrebleu.metrics import BLEU, CHRF, TER
from pymystem3 import Mystem
from prompts import Prompt
import re

load_dotenv()
deployment = os.environ.get("DEPLOYMENT")

# async method to get a candidate
async def get_candidate(reference, i, client, language):
  
  print(f"│coroutine {i} started│")

  prompt = Prompt(reference=reference, language=language)
  messages = prompt.get_messages()
  
  try:
    response = await client.chat.completions.create(model = deployment, messages = messages)
    result = response.choices[0].message.content
  except openai.APIConnectionError as e:
    print("│The server couldn't be reached")
    print(e.__cause__)
    result = ""
  except openai.RateLimitError as e:
    print("│A 429 status code was received; we should back off a bit.")
    result = ""
  except openai.APIStatusError as e:
    print("│Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
    result = ""

  if result is not None:
    if re.search('^"',result) and re.search('".$',result):    
      result = re.sub('^"', '', result, count = 1)
      result = re.sub('".$', '', result, count = 1)
    elif re.search('^"',result) and re.search('"$',result):
      result = re.sub('^"', '', result, count = 1)
      result = re.sub('"$', '', result, count = 1)
    
  print(f"candidate[{i}]{result}")
  return result

# async method to make a candidate_list variable
async def main(reference, client, language):
  
  tasks = []
  async with asyncio.TaskGroup() as tg:
    for i in range(3):
      task = tg.create_task(get_candidate(reference, i, client, language))
      tasks.append(task)

  results = [task.result() for task in tasks]

  return results

# get the highest score between all candidates
def get_highest_score(reference, client, language):
      
  candidate_list = []
  candidate_list = asyncio.run(main(reference, client, language)) 
  
  m = Mystem()
  hypotheses = m.lemmatize(reference)    
  max_score = 0.0 
  result = ""
  results = []

  print("┌─────────────────────────────────────────────────────────────┐")
  print("│chrf")
  for candidate in candidate_list:
    chrf = CHRF()
 
    if language != "kazakh": 
      try:
        ref = m.lemmatize(candidate)
      except AttributeError:
        ref = ""
    else:
      ref = candidate
    
    try:
      score_str = str(chrf.corpus_score(hypotheses=hypotheses, references=[ref,]))
      score_str = score_str.replace("chrF2 = ", "")
    except IndexError as e:
      print(f"│error for calculating candidate score '{candidate}': {e}")
      score_str = 0.0
    
    print(f"│{candidate} : {score_str}") 
    
    score = float(score_str)
    results.append({ "candidate": candidate, "score": score})
    
    if score > max_score:
      max_score = score
      result = candidate

  print("└─────────────────────────────────────────────────────────────┘") 
  
  if result == "":
    result = reference 
    results = ""
      
  return { "result": result, "results": results }


