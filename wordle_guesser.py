import word_lists.answers
import word_lists.guesses
import wordle_proxy
import Guess
import next_guess


def main_loop():
    answer_list = word_lists.answers.get_answers(scrambled=False)
    guess_list = word_lists.guesses.get_guesses()
    total_count = 0
    failed_puzzles = []
    failed_words = []
    # puzzles = [35, 42, 78, 130, 143, 191, 365, 385, 419, 468, 500, 509, 532, 534, 537, 555, 622, 652, 688, 701, 726, 730, 731, 803, 816, 848, 862, 890, 892, 1003, 1024, 1095, 1131, 1283, 1327, 1330, 1339, 1388, 1389, 1427, 1447, 1482, 1492, 1506, 1578, 1595, 1597, 1633, 1645, 1665, 1674, 1683, 1713, 1730, 1749, 1759, 1772, 1779, 1800, 1851, 1863, 1864, 1873, 1895, 1902, 1930, 1950, 2019, 2030, 2035, 2037, 2067, 2083, 2096, 2105, 2159, 2162, 2191, 2195, 2199, 2222, 2225, 2266, 2274, 2276, 2281, 2291, 2305, 2307]
    # puzzles = [42, 55, 666, 1066, 256, 354]
    # puzzles = [130]
    puzzles = range(0, len(answer_list))
    for puzzle in puzzles:
        print(f"Puzzle: {puzzle}")
        failed = False
        words = guess_list.copy()
        temp_words_list = words.copy()
        guess = Guess.Guess()
        count = 0
        guess.guess_result = ""

        while guess.guess_result != "win":
            print(f"words remaining: {len(words)}")
            if len(words) < 20:
                print(f"words remaining: {words}")
            if count == 0:
                guess.guess = "jumpy".lower()
                # guess.guess = "slice".lower()
            elif count == 1:
                guess.guess = "glint".lower()
                # guess.guess = "bayou".lower()
            elif count == 2:
                guess.guess = "brake".lower()
                # guess.guess = "bayou".lower()
            else:
                guess.guess = next_guess.select_next_guess(words, guess)
                # guess.guess = words[0]
            for letter in guess.guess:
                guess.guessed_letters.append(letter)
            guess.guess_result = wordle_proxy.validate(guess.guess, puzzle, answer_list)

            print(guess.guess)
            words = next_guess.manage_word_list(words, guess)
            count = count + 1
        if count > 6:
            failed = True
            failed_puzzles.append(puzzle)

        print(f"Puzzle: {puzzle}\nAttempts: {count}\nWord: {guess.guess}\n\n\n")
        # print(f"Puzzle: {puzzle}\nAttempts: {count}\n\n\n")
        if failed:
            total_count = total_count + 10
        else:
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




