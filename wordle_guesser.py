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
    # puzzles = [42, 55, 666, 1066, 256, 354]
    puzzles = [272]
    # puzzles = range(0, len(answers))
    for puzzle in puzzles:
        failed = False
        words = guess_list.copy()
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
            guess.guess_result = wordle_proxy.validate(guess.guess, puzzle, answer_list)
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




