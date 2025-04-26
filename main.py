import tkinter as tk
from tkinter import ttk
import random

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("8 Puzzle Game")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.config(bg="#EAEAEA")
        self._current_state = list(range(0, 9))
        random.shuffle(self._current_state)# 1-8 and None for empty space
        self.buttons = []
        # Title Label
        self.title_label = ttk.Label(
            self.root,
            text="8 Puzzle Game",
            font=("Arial", 24, "bold"),
        )
        self.title_label.pack()

        # Frame for the puzzle
        self.puzzle_frame = ttk.Frame(
            self.root
        )
        self.puzzle_frame.pack(pady=20)
        self.display_state()
        self.shuffle_button = ttk.Button(self.root,
                                        command=lambda row=3, col=3: random.shuffle(self._current_state),
                                        text="Shuffle", )
        self.shuffle_button.pack(pady=20)

        self.refresh_timer = 100
        self.refresh()
    def refresh(self):
        self.display_state()
        # noinspection PyTypeChecker
        self.root.after(self.refresh_timer, self.refresh)


    def current_state(self, new_state):
        self._current_state = new_state
        self.display_state()  # Automatically refresh display when state changes

    def display_state(self):
        # Clear existing buttons
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        # Recreate buttons with the current state
        counter = 0
        for i in range(3):
            for j in range(3):
                if self._current_state[counter] == 0:
                    counter += 1
                    continue
                else:
                    button = tk.Button(
                        self.puzzle_frame,
                        width=6,
                        height=3,
                        font=("Arial", 16, "bold"),
                        command=lambda row=i, col=j: "",
                        text=self._current_state[counter],
                    )
                    button.grid(row=i, column=j, padx=2, pady=2)
                    self.buttons.append(button)
                    counter += 1



gui = GUI()
gui.root.mainloop()

