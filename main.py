import tkinter as tk
from tkinter import ttk
import random
import tkinter.messagebox
import BackEND

class GUI:
    Goal = []

    def __init__(self):
#This is like the constructor of an object, with "self" is the same as this
#and every method takes parameter "self" as first parameter to make sure that when called it modifies the current object
        self.solution = None
        self.root = tk.Tk()
        self.root.title("8 Puzzle Game")
        self.root.geometry("800x500")
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
        
        self.input_Puzzle()
        self.refresh_timer = 100
        self.Solve = ttk.Button(
                self.root,command = lambda : self.solve(),
            text="Solve"
            )
        self.Solve.pack(pady=20)
    def solve(self):
        # Update Goal state from input buttons before solving
        GUI.Goal = []
        for btn in self.input_buttons:
            GUI.Goal.append(int(btn['text']))

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
                if Board[counter] == 0:
                    counter += 1
                    continue
                else:
                    button = tk.Button(
                        self.puzzle_frame,
                        width=6,
                        height=3,
                        font=("Arial", 16, "bold"),
                        command=lambda row=i, col=j: "",
                        text=Board[counter],
                    )
                    button.grid(row=i, column=j, padx=2, pady=2)
                    self.buttons.append(button)
                    counter += 1
    input_buttons = []
    def input_Puzzle(self):
        counter = 0
        def create_button_click(this_button):
            def button_click():
                current = int(this_button['text'])
                # Cycle through 0-8
                next_value = (current + 1) % 9
                this_button.config(text=str(next_value))
                # Update goal list every time a button is clicked
                GUI.Goal = []  # Reset the goal list
                for butn in self.input_buttons:
                    GUI.Goal.append(int(butn['text']))

            return button_click

        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.input_frame,
                    width=6,
                    height=3,
                    font=("Arial", 16, "bold"),
                    text=str(counter),
                )
                # Create a specific click handler for this button
                button['command'] = create_button_click(button)
                button.grid(row=i, column=j, padx=2, pady=2)
                self.input_buttons.append(button)
                counter += 1
    
        # Initialize Goal list with initial values
        GUI.Goal = []
        for btn in self.input_buttons:
            GUI.Goal.append(int(btn['text']))
    def goalset(self):
        for button in self.input_buttons:
            GUI.Goal.append(int(button['text']))


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