import random
import sys
import time
from pathlib import Path

Letters = "abcdefghijklmnopqrstuvwxyz"
Dir1 = "/usr/dict/words"
Dir2 = "/usr/share/dict/words"

def print_hex(sel):
  print(f"    {sel[0].upper()}")
  print(f"{sel[1].upper()}       {sel[2].upper()}")
  print(f"    {sel[3].upper()}   ")
  print(f"{sel[4].upper()}       {sel[5].upper()}")
  print(f"    {sel[6].upper()}")

# seems like reasonable default values, I've had games generated with over 300 words which would
# probably be frustrating for any but the most massochistic of logophiles
def generate_game(min_gamesize=10, max_gamesize=70):
  word_dir = Dir1 if Path(Dir1).exists() else Dir2 if Path(Dir2).exists() else None

  if word_dir is None:
    sys.exit("Couldn't find a dictionary file on your system.")

  word_file = open(word_dir)
  words = [line.strip() for line in word_file.readlines()]
  # filter out posssessive and proper nouns
  words = [word for word in words if "'" not in word and all([c.islower() for c in word])]

  game = {
    "letters" : [],
    "answers": [],
    "cnt" : 0,
    "guessed" : [],
    "common" : 0
  }

  start = time.time()

  while game["cnt"] < min_gamesize or game["cnt"] > max_gamesize:
    # if this is taking a bit, reward the user with a bee for their patience
    # only give out 1 per second, lest they become spoiled (and lest we run out of bees!)
    if time.time() - start > 1:
      print("🐝", end="", flush=True)
      start = time.time()

    letters = random.sample(Letters, 7)
    not_allowed = set(Letters).difference(set(letters))

    # ok now make the list of answer words
    common = letters[3]
    # get every word containing the common letter, not containing any letters outside the current letter set,
    # and only use words at least of length 4
    answers = [w for w in words if common in w \
               and len(w) > 3 and not any([na in w for na in not_allowed])]

    # filter out any words with accent characters
    answers = [a for a in answers if all([ord(c) < 128 for c in a])]

    # check that at least one of our answers contains every letter
    if not any([set(ans) == set(letters) for ans in answers]):
      continue

    game["letters"] = letters
    game["answers"] = answers
    game["cnt"] = len(answers)
    game["common"] = common

  return game

def print_help():
  print("Options: ")
  print('"-hex" : print the letter hex.')
  print('"-guessed" : print the words you\'ve guessed.')
  print('"-score" : Show your score out of total.')
  print('"-giveup" : Admit defeat, and see which words you hadn\'t guessed yet.')
  print('"-help" : Print these options.')

print("Bees...?🐝", end='', flush=True)
game = generate_game()

print()
print_hex(game["letters"])
print(f'\nTotal Words: {len(game["answers"])}\n')
print("How to play:\n")
print("Guess words until you win!")
print("Proper nouns are not included.")
print("All words are at least 4 letters.")
print("Every answer uses the letter in the middle of the letter hexagon above.")
print("There is at least 1 answer, which uses every letter.")
print("Your guesses are case-insensitive so don't worry about capitilization. There are no accented characters or silly gotchas.")
print("The number of answers which exist is noted above, and is hard coded to be between 10 and 70 because my author is lazy.\n")
print_help()

while len(game["guessed"]) < game["cnt"]:
  guess = input("Guess a word: ")

  if not len(guess):
    continue

  if guess[0] == '-':
    option = guess[1:]
    if option == "hex":
      print_hex(game["letters"])
    elif option == "guessed":
      print(game["guessed"])
    elif option == "score":
      print(f'{len(game["guessed"])} / {game["cnt"]}')
    elif option == "help":
      print_help()
    elif option == "giveup":
      print(f'Lame!\n')
      print(f'You have guessed:')
      for g in game["guessed"]:
        print(g, end=' ')
      print(f'\n\nRemaining words were:')
      for a in game["answers"]:
        print(a, end=' ')
        if set(a) == set(game["letters"]):
          print("(<= contains all letters) ", end='')
      sys.exit("\nExiting, re-run me to play again.")
    else:
      print(f"{option}, not an option")
    continue

  guess = guess.lower()
  if guess in game["answers"]:
    print("Nice, that's an answer!")
    game["guessed"].append(guess)
    game["answers"].remove(guess)
  elif guess in game["guessed"]:
    print("Already guessed!")
  elif not guess.isalpha():
    print("Alphabetic words only!")
  elif len(guess) < 4:
    print(f"All answers are at least 4 letters.")
  elif game["common"] not in guess:
    print(f'All answers will contain "{game["common"].upper()}".')
  else:
    print("Not a word, or not in the answers.")

print("You won!")
