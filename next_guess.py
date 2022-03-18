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