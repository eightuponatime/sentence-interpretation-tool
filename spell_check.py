#required python developer package
#sudo apt-get install python3.12-dev

from spellchecker import SpellChecker

from pathlib import Path
from symspellpy import SymSpell, Verbosity

# spell checker for russian and english

def spell_check(reference, language):
  spell = SpellChecker()
  
  match language:
    case "en":
      spell = SpellChecker()
    case "ru":
      spell = SpellChecker(language = language)

  words = reference.split(' ')

  result = []

  for word in words:
    misspelled = spell.unknown([word])
    if misspelled:
      new_word = spell.correction(word)
      if new_word is None:
        new_word = ""
      result.append(new_word)
    else:
      result.append(word)

  joined_words = " ".join(result)
  
  print("┌─────────────────────────────────────────────────────────────┐")
  print(f"│spell check")
  print(f"│reference: {reference}")
  print(f"│result: {joined_words}")
  print("└─────────────────────────────────────────────────────────────┘") 

  return joined_words

# spell checker for kazakh language

MAX_EDIT_DISTANCE = 2 
DICTIONARY_PATH = Path('./kk.txt') 

symspell = SymSpell(max_dictionary_edit_distance = MAX_EDIT_DISTANCE)
symspell.load_dictionary(DICTIONARY_PATH, term_index=0, count_index=1, encoding='utf-8')

def lookup_word(word, verbosity, max_edit_distance):
  suggestions = symspell.lookup(word, verbosity, max_edit_distance)
  words_list = [item.term for item in suggestions]
  
  if verbosity == Verbosity.CLOSEST:
    return words_list

  if len(words_list) > 0:
    return words_list[0]
  
  return None

def kk_lookup(word):  
  closest_words = lookup_word(word, Verbosity.CLOSEST, MAX_EDIT_DISTANCE)
  most_frequent_word = lookup_word(word, Verbosity.TOP, MAX_EDIT_DISTANCE)
  
  return most_frequent_word

def kazakh_spell_check(reference):
  words = reference.split(' ')
  result = []
  
  for word in words:
    spell_check = kk_lookup(word)
    result.append(spell_check)
  
  joined_words = " ".join(result)

  print("┌─────────────────────────────────────────────────────────────┐")
  print(f"│spell check")
  print(f"│reference: {reference}")
  print(f"│result: {joined_words}")
  print("└─────────────────────────────────────────────────────────────┘") 

  return joined_words
 
