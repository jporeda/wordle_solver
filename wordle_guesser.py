import wordle_proxy
import Guess
import next_guess
import get_words


def main_loop():
    answers = get_words.get_words(answers_only=True)
    orig_words = get_words.get_words(answers_only=False)
    total_count = 0
    failed_puzzles = []
    failed_words = []
    # puzzles = [42, 55, 666, 1066, 256, 354]
    puzzles = [272]
    # puzzles = range(len(answers)-3, len(answers))
    # puzzles = [27, 191, 429, 664, 670, 692, 793, 802, 803, 848, 862, 878, 923, 952, 1061, 1072, 1079, 1205, 1222, 1343, 1361, 1370, 1427, 1495, 1524, 1640, 1665, 1674, 1678, 1683, 1713, 1757, 1784, 1849, 1851, 1863, 1868, 1873, 1885, 1932, 1945, 1959, 1965, 1992, 2030, 2037, 2050, 2056, 2086, 2112, 2119, 2167, 2170, 2191, 2199, 2220, 2252, 2268, 2274, 2287, 2298, 2305, 2308]
    # puzzles = range(0, len(answers))
    for puzzle in puzzles:
        failed = False
        words = orig_words.copy()
        guess = Guess.Guess()
        count = 0
        guess.guess_result = ""

        while guess.guess_result != "win":
            print(f"words remaining: {len(words)}")
            if count == 0:
                guess.guess = "slice".lower()
            else:
                guess.guess = next_guess.select_next_guess(words, guess)
                # guess.guess = words[0]
            for letter in guess.guess:
                guess.guessed_letters.append(letter)
            # guess.guess_result = submit_request(guess.guess, puzzle)
            print(guess.guess)
            guess.guess_result = wordle_proxy.validate(guess.guess, puzzle, answers)
            words = next_guess.manage_word_list(words, guess)
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




