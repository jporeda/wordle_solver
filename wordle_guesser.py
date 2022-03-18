import requests
import os
import json
import cProfile

class Guess:
    def __init__(self):
        self.guess = ""
        self.guess_result = []
        self.guessed_letters = []


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


def validate(word, puzzle, answers):
    # words = get_words(answers_only=True)
    words = answers
    answer = words[puzzle]
    letters = list(word.lower())
    answer_letters = list(answer)
    response = [None]*5
    green_letters = []
    correct_indexes = []
    # green letters
    for ix, letter in enumerate(letters):
        if letter == answer_letters[ix]:
            correct_indexes.append(ix)
            green_letters.append(letter)
            response[ix] = 'G'
    # yellow letters
    for ix, letter in enumerate(letters):
        green_letter_count = green_letters.count(letter)
        answer_letter_count = answer_letters.count(letter)
        if green_letter_count >= answer_letter_count:
            continue
        if letter in answer and ix not in correct_indexes:
            response[ix] = 'Y'

    if response.count("G") == 5:
        return "win"
    else:
        return response


def submit_request(guess, index=0):
    url = "https://api-us.kitewheel.com/api/v1/listener/f4a32cbeffa61b0165c34c75d10306a3"
    guess_json = {
        "puzzleId": index,
        "word": guess
    }
    response = requests.post(url=url, json=guess_json)

    if "win" in response.text:
        return "win"
    if "word" in response.text:
        return "error"
    else:
        return json.loads(response.text)


def manage_word_list(words, guess):
    iter_list = words.copy()
    for index, value in enumerate(guess.guess_result):
        # remove all words where the value is None for this exact position
        # this does not have a duplicate letter issue because we take position into account
        for word in iter_list:
            if value is None:
                if word[index] == guess.guess[index]:
                    if word in words:
                        words.remove(word)
            if value == "G":
                if word[index] != guess.guess[index]:
                    if word in words:
                        words.remove(word)
            if value == "Y":
                # remove words where we know a letter is there, but not where
                if guess.guess[index] not in word:
                    if word in words:
                        words.remove(word)
                # remove words where we know a letter is in the word, but its not right here
                if guess.guess[index] == word[index]:
                    if word in words:
                        words.remove(word)

    # for index, value in enumerate(guess.guess_result):
    #     # remove all words where the value is None for this exact position
    #     # this does not have a duplicate letter issue because we take position into account
    #     if value is None:
    #         for word in iter_list:
    #             if word[index] == guess.guess[index]:
    #                 if word in words:
    #                     words.remove(word)
    #     # remove all words where we don't match known greens
    #     if value == "G":
    #         for word in iter_list:
    #             if word[index] != guess.guess[index]:
    #                 if word in words:
    #                     words.remove(word)
    #     if value == "Y":
    #         for word in iter_list:
    #             # remove words where we know a letter is there, but not where
    #             if guess.guess[index] not in word:
    #                 if word in words:
    #                     words.remove(word)
    #             # remove words where we know a letter is in the word, but its not right here
    #             if guess.guess[index] == word[index]:
    #                 if word in words:
    #                     words.remove(word)

    # final remove- word that is left that has a guessed null, that is not a duplicate letter
    # get the nulls first
    null_letters = []
    not_null_letters = []
    for index, value in enumerate(guess.guess_result):
        if value is None and guess.guess[index] not in null_letters:
            null_letters.append(guess.guess[index])
        else:
            not_null_letters.append(guess.guess[index])
    for let in not_null_letters:
        if let in null_letters:
            null_letters.remove(let)

    for word in iter_list:
        if any(x in list(word) for x in null_letters):
            if word in words:
                words.remove(word)
                pass

    return words


def remove_duplicate_letters(word):
    new_word = ""

    for letter in word:
        if letter not in new_word:
            new_word = new_word + letter

    return new_word


def select_next_guess(words, guess):
    next_guess = None
    five_new = []
    four_new = []
    three_new = []
    two_new = []
    one_new = []

    for word in words:
        de_duped_word = remove_duplicate_letters(word)
        new_letters = len(de_duped_word)
        for letter in de_duped_word:
            if letter in guess.guessed_letters:
                new_letters = new_letters - 1
        if new_letters == 5:
            five_new.append(word)
        elif new_letters == 4:
            four_new.append(word)
        elif new_letters == 3:
            three_new.append(word)
        elif new_letters == 2:
            two_new.append(word)
        else:
            one_new.append(word)

    if len(five_new) > 0:
        next_guess = find_best_option_in_next_guess(five_new)
    elif len(four_new) > 0:
        next_guess = find_best_option_in_next_guess(four_new)
    elif len(three_new) > 0:
        next_guess = find_best_option_in_next_guess(three_new)
    elif len(two_new) > 0:
        next_guess = find_best_option_in_next_guess(two_new)
    else:
        next_guess = find_best_option_in_next_guess(one_new)
    return next_guess


def find_best_option_in_next_guess(guess_list):
    for word in guess_list:
        if word[-2:] == "er":
            return word
    for word in guess_list:
        if "ud" in list(word):
            return word
    for word in guess_list:
        if "u" in list(word):
            return word
    for word in guess_list:
        if "un" in list(word):
            return word
    for word in guess_list:
        if "a" in word:
            return word
    for word in guess_list:
        if "un" in list(word):
            return word
    for word in guess_list:
        if "ou" in list(word):
            return word
    for word in guess_list:
        if "r" in list(word):
            return word
    for word in guess_list:
        if "a" in list(word):
            return word
    for word in guess_list:
        if "y" in list(word):
            return word

    return guess_list[0]


def main_loop():
    answers = get_words(answers_only=True)
    orig_words = get_words(answers_only=False)
    total_count = 0
    failed_puzzles = []
    failed_words = []
    # puzzles = [42, 55, 666, 1066, 256, 354]
    # puzzles = [692]
    # puzzles = range(len(answers)-3, len(answers))
    # puzzles = [27, 191, 429, 664, 670, 692, 793, 802, 803, 848, 862, 878, 923, 952, 1061, 1072, 1079, 1205, 1222, 1343, 1361, 1370, 1427, 1495, 1524, 1640, 1665, 1674, 1678, 1683, 1713, 1757, 1784, 1849, 1851, 1863, 1868, 1873, 1885, 1932, 1945, 1959, 1965, 1992, 2030, 2037, 2050, 2056, 2086, 2112, 2119, 2167, 2170, 2191, 2199, 2220, 2252, 2268, 2274, 2287, 2298, 2305, 2308]
    puzzles = range(0, len(answers))
    for puzzle in puzzles:
        failed = False
        words = orig_words.copy()
        guess = Guess()
        count = 0
        guess.guess_result = ""

        while guess.guess_result != "win":
            print(f"words remaining: {len(words)}")
            if count == 0:
                guess.guess = "slane".lower()
            # elif count == 1:
            #     guess.guess = "bayou"
            else:
                guess.guess = select_next_guess(words, guess)
                # guess.guess = words[0]
            for letter in guess.guess:
                guess.guessed_letters.append(letter)
            # guess.guess_result = submit_request(guess.guess, puzzle)
            print(guess.guess)
            guess.guess_result = validate(guess.guess, puzzle, answers)
            words = manage_word_list(words, guess)
            count = count + 1
        if count > 6:
            failed = True
            failed_puzzles.append(puzzle)
            # count = count + 10
            # break
        print(f"Puzzle: {puzzle}\nAttempts: {count}\nWord: {guess.guess}\n\n\n")
        # print(f"Puzzle: {puzzle}\nAttempts: {count}\n\n\n")
        total_count = total_count + count
        if failed is True:
            failed_words.append(guess.guess)

    print(total_count / len(puzzles))
    print(f'Failed Words: {failed_words}')
    print(f'Failed Puzzles: {failed_puzzles}')
    print(f'Total Failed Puzzles: {len(failed_words)}')
    print(f'Total Puzzles: {len(puzzles)}')



if __name__ == '__main__':
    main_loop()
    # cProfile.run('main_loop()')




