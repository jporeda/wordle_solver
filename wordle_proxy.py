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