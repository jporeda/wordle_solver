import os
import json

def get_words(answers_only=True):
    words_file = open(os.path.expanduser("C:/Users/Jeff/PycharmProjects/wordle/wordle_answers_scrambled.json"), "r")
    words = json.loads(words_file.read())
    words_file.close()

    if not answers_only:
        additional_words = open(os.path.expanduser("C:/Users/Jeff/PycharmProjects/wordle/wordle_guesses.json"), "r")
        additional_words_parsed = json.loads(additional_words.read())
        additional_words.close()
        words = words + additional_words_parsed

    return words