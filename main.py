import tkinter as tk
from tkinter import ttk
import random
import tkinter.messagebox
import BackEND
from PIL import Image, ImageTk


class GUI:
    Goal = [1,2,3,4,5,6,7,8,0]

    def __init__(self):
#This is like the constructor of an object, with "self" is the same as this
#and every method takes parameter "self" as first parameter to make sure that when called it modifies the current object
        self.solution = None
        self.root = tk.Tk()
        self.root.title("8 Puzzle Game")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.root.config(bg="#EAEAEA")
# Load and resize images
        self.images = {}
        for i in range(9):  # 0-8
            image = Image.open(f"Photos/image_part_00{i}.jpg")
            # Resize image to fit buttons (adjust size as needed)
            image = image.resize((60, 60), Image.Resampling.LANCZOS)
            self.images[i] = ImageTk.PhotoImage(image)


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

        # Create a container frame to hold both frames
        self.container_frame = ttk.Frame(self.root)
        self.container_frame.pack(pady=20)

        # Frame for the puzzle
        self.puzzle_frame = ttk.Frame(self.container_frame)
        self.puzzle_frame.grid(row=0, column=0, padx=10)

        # Frame for input
        self.input_frame = ttk.Frame(self.container_frame)
        self.input_frame.grid(row=0, column=1, padx=10)

        self.display_state(self._current_state)
        self.shuffle_button = ttk.Button(
        self.root,
        command=self.shuffle_puzzle,  # Change to new method
        text="Shuffle"
    )
        self.shuffle_button.pack(pady=20)

        self.Solve = ttk.Button(
                self.root,command = lambda : self.solve(),
            text="Solve"
            )
        self.Solve.pack(pady=20)
    def solve(self):
        self.solution = self.A_Star(self._current_state)
        if self.solution:
            self.PrintSolution(Solution=self.solution)
            self._current_state = GUI.Goal
        else:
            tk.messagebox.showinfo("Error", "Puzzle is unsolvable")
    def display_state(self,Board):
        # Clear existing buttons
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        # Recreate buttons with the current state
        counter = 0
        for i in range(3):
            for j in range(3):
                    button = tk.Button(
                        self.puzzle_frame,
                        width=60,
                        height=60,
                        image=self.images[Board[counter]],
                        command=lambda row=i, col=j: "",
                    )
                    button.grid(row=i, column=j, padx=2, pady=2)
                    self.buttons.append(button)
                    counter += 1


    @staticmethod
    def A_Star(StartState):
        PriorityQueue = []  # This will be our priority queue.
        Visited = set()  # This will be our visited states.

        # This will be our initial state.
        # We will push the initial state to the priority queue
        #  with our start state and its heuristic value.
        BackEND.heapq.heappush(PriorityQueue, BackEND.PuzzleState(StartState, None, None, 0, BackEND.heuristic(StartState, GUI.Goal)))
        while PriorityQueue:
            CurrentState = BackEND.heapq.heappop(PriorityQueue)  # Pops the state with the lowest cost.
            if CurrentState.Board == GUI.Goal:
                return CurrentState  # If the current state is the goal state, we will return it.

            Visited.add(tuple(CurrentState.Board))  # Add the current state to the visited states.
            GapPos = CurrentState.Board.index(0)  # Get the index of the gap in the current state.
            for Move in BackEND.moves:
                if Move == 'U' and GapPos < 3: continue
                if Move == 'D' and GapPos > 5: continue
                if Move == 'L' and GapPos % 3 == 0: continue
                if Move == 'R' and GapPos % 3 == 2: continue
                NewBoard = BackEND.move_element(CurrentState.Board, Move, GapPos)  # Makes a new board with the move.
                # If the new board is already visited, we will skip it.
                if tuple(NewBoard) in Visited: continue
                # If the new board is not visited, we will create a new state for it.
                # We will push the new state to the priority queue with its new values.
                NewState = BackEND.PuzzleState(NewBoard, CurrentState, Move, CurrentState.Depth + 1,
                                       CurrentState.Depth + 1 + BackEND.heuristic(NewBoard, GUI.Goal))
                BackEND.heapq.heappush(PriorityQueue, NewState)
        return None  # If we reach here, it means we couldn't find a solution.
        # This will occur if the puzzle is unsolvable.
        # This will happen if the number of inversions is odd.
        # An inversion is a pair of tiles that are in the wrong order [like 1,2,3,4,5,6,*8*,*7*,0]
        #  the number of inversions in this case is 1 because 8[greater] comes before 7[smaller]
        #   which is odd so the puzzle is unsolvable.

    def PrintSolution(self, Solution):
        Path = []
        CurrentState = Solution
        while CurrentState:
            Path.append(CurrentState)
            CurrentState = CurrentState.Parent
        Path.reverse()

        def update_step(index):
            if index < len(Path):
                step = Path[index]
                self.display_state(step.Board)
                self.root.after(1000, update_step, index + 1)
            else:
                # Show "Solved" message after the last update
                tk.messagebox.showinfo("Success", "Puzzle Solved!")

        update_step(0)

    def shuffle_puzzle(self):
        # Shuffle the current state
        random.shuffle(self._current_state)
        # Update the display with new shuffled state
        self.display_state(self._current_state)


if __name__ == "__main__":
    gui = GUI()
    gui.root.mainloop()