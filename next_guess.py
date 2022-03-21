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
    ranked_words = []

    for word in words:
        de_duped_word = remove_duplicate_letters(word)
        new_letters = len(de_duped_word)
        for letter in de_duped_word:
            if letter in guess.guessed_letters:
                new_letters = new_letters - 1
        ranked_words.append((word, new_letters))
    next_guess = find_best_option_in_next_guess(ranked_words)

    return next_guess


def list_sort_helper(word_with_rank):
    return word_with_rank[1]


def find_best_option_in_next_guess(guess_list):
    guess_list.sort(key=list_sort_helper, reverse=True)


    for word in guess_list:
        if word[0][-2:] == "er":
            return word[0]
    for word in guess_list:
        if "r" in list(word[0]):
            return word[0]
    for word in guess_list:
        if "ud" in list(word[0]):
            return word[0]
    for word in guess_list:
        if "u" in list(word[0]):
            return word[0]
    # for word in guess_list:
    #     if "un" in list(word):
    #         return word
    # for word in guess_list:
    #     if "a" in word:
    #         return word
    # for word in guess_list:
    #     if "un" in list(word):
    #         return word
    # for word in guess_list:
    #     if "ou" in list(word):
    #         return word
    # for word in guess_list:
    #     if "r" in list(word):
    #         return word
    # for word in guess_list:
    #     if "a" in list(word):
    #         return word
    # for word in guess_list:
    #     if "y" in list(word):
    #         return word

    return guess_list[0][0]