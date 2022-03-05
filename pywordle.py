import signal
import tkinter as tk
from tkinter import messagebox

import enchant

ENGLISH_WORDS = enchant.Dict("en_US")
MAX_GUESSES = 6
GAME_WORD_LENGTH = 5
LARGE_FONT = "Helvetica 30 bold"
MEDIUM_FONT = "Helvetica 20 bold"


def play_pywordle():
    guess_count = 0
    game_word = None
    replay = game_over = False

    def _submit_input(event=None):
        """
        Grabs the current value of the "word_input" entry widget.
        If "game_word" is not set, sets "game_word" and starts a new game.
        If "game_word" is set, processes the entered text as a word guess.
        """
        nonlocal guess_count, game_word, replay, game_over
        entered_word = word_input.get().upper()
        if not _valid_word(entered_word):
            tk.messagebox.showerror("Invalid word", "You did not enter a valid 5-character word. Try again.")
            return

        # If game word is set, that means game has started and word submissions are guesses
        if game_word:
            if ENGLISH_WORDS.check(entered_word):
                for idx, letter in enumerate(entered_word):
                    tile = word_tiles_idx[guess_count][idx]
                    tile["text"] = letter
                    if letter == game_word[idx]:
                        tile.config(bg="green", fg="white")
                    elif letter in game_word:
                        tile.config(bg="yellow", fg="white")
                    else:
                        tile.config(bg="gray", fg="white")
                guess_count += 1
            else:
                messagebox.showerror("Invalid word", "Your guess was not a valid word! Try again.")
        # First valid entered word is for setting the secret game word to start the game.
        else:
            game_word, entered_word = entered_word, None
            messagebox.showinfo("Game start!", "Player 2, it's your turn to guess!")
            # One secret game word is set, user input can be unmasked
            word_input.config(show="")

        game_msg["text"] = f"Guesses remaining: {MAX_GUESSES - guess_count}"

        if entered_word == game_word:
            game_over = True
            replay = messagebox.askyesno("Winner!", "You win! Would you like to play again?")

        if guess_count >= MAX_GUESSES:
            game_over = True
            replay = messagebox.askyesno("Game over", "Game over man! Would you like to play again?")

        if game_over:
            if replay:
                _start_new_game()
            else:
                ui_root.destroy()
                return

        # Clear the input text so player can try another guess
        word_input.delete(0, tk.END)

    def _start_new_game():
        """
        Resets game state so that a new game can be played
        """
        nonlocal guess_count, game_word, replay, game_over
        guess_count = 0
        game_word = None
        replay = game_over = False
        game_msg["text"] = "Player 1, enter a 5-character word:"
        word_input.config(show="*")
        for row in word_tiles_idx:
            for tile in row:
                tile.config(height=2, width=4, borderwidth=2, relief="solid", font=LARGE_FONT, bg="white")
                tile["text"] = ""

    ui_root = tk.Tk()
    ui_root.title("Pywordle")
    # ui_root.eval('tk::PlaceWindow . center')
    ui_root.bind('<Return>', _submit_input)

    # Makes it so that input field only accepts at most MAX_WORD_LENGTH characters
    input_len_constraint = (ui_root.register(lambda word: len(word) <= GAME_WORD_LENGTH), '%P')

    game_msg = tk.Label(ui_root, font=MEDIUM_FONT)
    game_msg.pack(anchor="w", padx=10)

    words_board = tk.Frame(ui_root)
    words_board.pack(padx=10)
    word_tiles_idx = [[None for i in range(GAME_WORD_LENGTH)] for j in range(MAX_GUESSES)]
    for row in range(MAX_GUESSES):
        for col in range(GAME_WORD_LENGTH):
            tile = tk.Label(words_board)
            tile.grid(row=row, column=col, padx=2, pady=4)
            # Store reference to letter tiles so that we can update them throughout the game
            word_tiles_idx[row][col] = tile

    word_input = tk.Entry(ui_root, validate="key", validatecommand=input_len_constraint, font=LARGE_FONT)
    word_input.pack(fill="x", padx=10, pady=10)
    word_input.focus()

    _start_new_game()
    ui_root.mainloop()


def _valid_word(word):
    if word:
        return ENGLISH_WORDS.check(word) and len(word) == GAME_WORD_LENGTH
    return False


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    play_pywordle()
