class Prompt:

  reference = ""
  language = ""

  def __init__(self, reference, language):
    self.reference = reference,
    self.language = language
  
  def get_messages(self):
    
    russianPrompt = [
      {
        "role": "system",
        "content": f"Ты учитель русского языка",
      },
      {
        "role": "user",
        "content": ("Исправь смысловые ошибки в тексте: \"Моя любить дети\"." + 
        "Нужен именно самый правильный вариант с точки зрения носителя языка." + 
        "Важно чтобы в качестве ответа ты вывел просто самую верную интерпретацию" + 
        "этого предложения, и никаких слов больше. Даже если оно не имеет смысла," + 
        "приведи самый близкий по-твоему вариант. Любым способом избегай фразы:" + 
        f"\"это предложение не имеет смысла\" и подобное."+
        "Представь только полученный текст без лишних комментариев от тебя." + 
        "Не нужно никаких примечаний, только голый полученный текст"),
      },
      {
        "role": "assistant",
        "content": "Я люблю детей.",
      },
      {
        "role": "user",
        "content": (f"Исправь смысловые ошибки в тексте: \"{self.reference}\"." + 
        "Нужен именно самый правильный вариант с точки зрения носителя языка." + 
        "Важно чтобы в качестве ответа ты вывел просто самую верную интерпретацию" + 
        "этого предложения,и никаких слов больше. Даже если оно не имеет смысла," + 
        "приведи самый близкий по-твоему вариант. Любым способом избегай фразы:" +
        f"\"это предложение не имеет смысла\" и подобное."+
        "Представь только полученный текст без лишних комментариев от тебя." + 
        "Не нужно никаких примечаний, только голый полученный текст"),
      },
    ]

    englishPrompt= [
      {
        "role": "system",
        "content": f"You are a teacher of english language.",
      },
      {
        "role": "user",
        "content": (f"Correct semantic error in the text: \"my is like children\"." +
        "I need the most correct option from the point of view of a native speaker." +
        "It's important that as an answer you simply output the most correct interpretation" +
        "of this sentence, and no more words. Even if it doesn't make sendse," + 
        "give me the closes version in your opinion. Avoid the phrase in ane way:" +
        "\"this sentence doesn't make sense\" and the like." + 
        "Print only the received text without unnecessary comments from you" + 
        "No notes are needed, only the received text is needed."),
      },
      {
        "role": "assistant",
        "content": "I like children.",
      },
      {
        "role": "user",
        "content": (f"Correct semantic error in the text: \"{self.reference}\"." +
        "I need the most correct option from the point of view of a native speaker." +
        "It's important that as an answer you simply output the most correct interpretation" +
        "of this sentence, and no more words. Even if it doesn't make sendse," + 
        "give me the closes version in your opinion. Avoid the phrase in ane way:" +
        "\"this sentence doesn't make sense\" and the like." + 
        "Print only the received text without unnecessary comments from you" + 
        "No notes are needed, only the received text is needed."),
      },
    ]

    kazakhPrompt = [
      {
        "role": "system",
        "content": f"Ты учитель казахского языка",
      },
      {
        "role": "user",
        "content": ("Исправь смысловые ошибки в тексте на казахском: \"Мен сен жақсы.\"." + 
        "Нужен именно самый правильный вариант с точки зрения носителя языка." + 
        "Важно чтобы в качестве ответа ты вывел просто самую верную интерпретацию" + 
        "этого предложения, и никаких слов больше. Даже если оно не имеет смысла," + 
        "приведи самый близкий по-твоему вариант. Любым способом избегай фразы:" + 
        f"\"это предложение не имеет смысла\" и подобное."+
        "Представь только полученный текст без лишних комментариев от тебя." + 
        "Не нужно никаких примечаний, только голый полученный текст"),
      },
      {
        "role": "assistant",
        "content": "Мен сені жақсы көремін.",
      },
      {
        "role": "user",
        "content": (f"Исправь смысловые ошибки в тексте на казахском: \"{self.reference}\"." + 
        "Нужен именно самый правильный вариант с точки зрения носителя языка." + 
        "Важно чтобы в качестве ответа ты вывел просто самую верную интерпретацию" + 
        "этого предложения,и никаких слов больше. Даже если оно не имеет смысла," + 
        "приведи самый близкий по-твоему вариант. Любым способом избегай фразы:" +
        f"\"это предложение не имеет смысла\" и подобное."+
        "Представь только полученный текст без лишних комментариев от тебя." + 
        "Не нужно никаких примечаний, только голый полученный текст"),
      },
    ]


    """kazakhPrompt = [
      {
        "role": "system",
        "content": f"Сен қазақ тілі мұғалімсің."
      },
      {
        "role": "user",
        "content": (f"Мәтіндегі мағыналық қателерді түзет: \"Мен сен жақсы.\"." +
        "Тіл иесі тұрғысынан ең дұрыс нұсқасы керек." +
        "Жауап ретінде ең дұрыс интерпретацияны шығару маңызды, және артық сөздер болмауы керек." + 
        "Егер ол мағынасы жоқ болса да, ең жақын нұсқасын келтір." + 
        "\"Бұл сөйлемнің мағынасы жоқ\" деген сияқты фразалардан аулақ бол." + 
        "Артық түсіндірмелерсіз тек алынған мәтінді шығар." + 
        "Ешқандай ескертулер қажет емес, тек алынған мәтін ғана."),
      },
      {
        "role": "assistant",
        "content": "Мен сені жақсы көремін.",
      },
      {
        "role": "user",
        "content": (f"Мәтіндегі мағыналық қателерді түзет: \"{self.reference}\"." +
        "Тіл иесі тұрғысынан ең дұрыс нұсқасы керек." +
        "Жауап ретінде ең дұрыс интерпретацияны шығару маңызды, және артық сөздер болмауы керек." + 
        "Егер ол мағынасы жоқ болса да, ең жақын нұсқасын келтір." + 
        "\"Бұл сөйлемнің мағынасы жоқ\" деген сияқты фразалардан аулақ бол." +
        "Артық түсіндірмелерсіз тек алынған мәтінді шығар." + 
        "Ешқандай ескертулер қажет емес, тек алынған мәтін ғана."),
      }
    ]"""
    

    match self.language:
      case "ru":
        return russianPrompt
      case "kk":
        return kazakhPrompt
      case "en":
        return englishPrompt
  
      

