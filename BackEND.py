import heapq
import tkinter
from tkinter import messagebox
from main import GUI


# ------------------------------------------------------------------------------------#
#     AI Project: 8 Puzzle Solver [A* Search Algorithm] Team:خليها علي الله         #
# ------------------------------------------------------------------------------------#

# This class represents a state in our puzzle.
# Which carries the shape of the board, the parent state before our current state,
#  the move that led us to this state from the parent state, the depth of the state
#   from our initial state or in another name the G(n) value which means the number
#    of moves we have made to reach this state from the initial state, and the cost
#     of the state which is the sum of the depth and the huristic value of the state.
# Depth is G(n) and Cost is F(n) = G(n) + H(n).
# H(n) is the sum of the distances of the tiles from their goal position.
# The cost is used to sort the states in the priority queue by thier weights.


# Now we will define the PuzzleState class which we were talking about above.
# Step (1): Creating the class.

class PuzzleState:
    # this acts as a constructor for the class.
    # It initializes the class with the given parameters.
    def __init__(self, Board, Parent, Move, Depth, Cost):
        self.Board = Board
        self.Parent = Parent
        self.Move = Move
        self.Depth = Depth
        self.Cost = Cost

    # This function is used to compare two PuzzleState objects based on their cost.
    # It returns true if the cost of its object state is less that
    #  the other state in cost.
    def __lt__(self, Other):
        return self.Cost < Other.Cost


# Now we will make a method that prints the state of the board.
# As a simple UI.
def PrintBoard(Board):
    print("*=========*")  # The upper border.
    for row in range(0, 9, 3):  # Index [0,3,6] to start the rows.
        print("||", end="")  # The each left row border.
        for element in Board[row:row + 3]:
            if element == 0:  # If the element is 0, so this is the gap.
                print("-", end=" ")
            else:
                print("-", end=str(element))
        print("-||")  # The each right row border.
    print("*=========*")  # The bottom border.


###

# This [moves] is a dictionary that contains the possible moves we can make
#  and the values of it.
# Dictionary datatype is consists of [key, value] pairs
#  which we can store a value and call it by the key directly
#   moves is the difference between the current index and the next index we
#    need to get to after the move.
# For example if we need to go up from index 4 [middle element] to
#  index 1 [top middle element] we will subtract 3 from the current index
#   so if we need to go Up we will subtract 3 from the current index.
moves = {
    # keys : values
    'U': -3,  # Move up
    'D': 3,  # Move down
    'L': -1,  # Move left
    'R': 1  # Move right
}


# Here we will compare the current state with the goal state.
# [divmod] is a function that takes two numbers and returns the quotient and remainder
#  we use it to transform the linear index to 2D coordinates
#   the quotient is the row which is a complete 3 elements // divided by 3
#    and the remainder is what rmains after taking the completed rows which is column.
# For example if we have 5 and 2, it will return (2,1) because 5/2 = 2 and 5%2 = 1.
# We will use this to get the x and y coordinates of the current index.
# [index] is a function that returns the index of the element in the list.
# We will use it to get the index of the element we need to compare in the goal state.
def heuristic(Board, Goal):
    distance = 0
    for i in range(9):
        if Board[i] != 0:
            x1, y1 = divmod(i, 3)
            if (Board[i] not in Goal):
                tkinter.messagebox.showinfo("Error", f"{Board[i]} is not in Goal")
            goal_index = Goal.index(Board[i])
            x2, y2 = divmod(goal_index, 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


def move_element(Board, Move, GapPos):  # GapPos is its Index.
    NewBoard = Board[:]  # This will create a new board as a copy from our board.
    NewGapPos = GapPos + moves[Move]  # This will get the new position of the gap.

    # This will swap the gap's position with its new position.
    NewBoard[GapPos], NewBoard[NewGapPos] = NewBoard[NewGapPos], NewBoard[GapPos]
    return NewBoard


def A_Star(StartState):
    PriorityQueue = []  # This will be our priority queue.
    Visited = set()  # This will be our visited states.

    # This will be our initial state.
    # We will push the initial state to the priority queue
    #  with our start state and its huristic value.
    heapq.heappush(PriorityQueue, PuzzleState(StartState, None, None, 0, heuristic(StartState, GUI.Goal)))
    while PriorityQueue:
        CurrentState = heapq.heappop(PriorityQueue)  # Pops the state with the lowest cost.
        if CurrentState.Board == GUI.Goal:
            return CurrentState  # If the current state is the goal state, we will return it.

        Visited.add(tuple(CurrentState.Board))  # Add the current state to the visited states.
        GapPos = CurrentState.Board.index(0)  # Get the index of the gap in the current state.
        for Move in moves:
            if Move == 'U' and GapPos < 3: continue
            if Move == 'D' and GapPos > 5: continue
            if Move == 'L' and GapPos % 3 == 0: continue
            if Move == 'R' and GapPos % 3 == 2: continue
            NewBoard = move_element(CurrentState.Board, Move, GapPos)  # Makes a new board with the move.
            # If the new board is already visited, we will skip it.
            if tuple(NewBoard) in Visited: continue
            # If the new board is not visited, we will create a new state for it.
            # We will push the new state to the priority queue with its new values.
            NewState = PuzzleState(NewBoard, CurrentState, Move, CurrentState.Depth + 1,
                                   CurrentState.Depth + 1 + heuristic(NewBoard, GUI.Goal))
            heapq.heappush(PriorityQueue, NewState)
    return None  # If we reach here, it means we couldn't find a solution.
    # This will occur if the puzzle is unsolvable.
    # This will happen if the number of inversions is odd.
    # An inversion is a pair of tiles that are in the wrong order [like 1,2,3,4,5,6,*8*,*7*,0]
    #  the number of inversions in this case is 1 because 8[greater] comes before 7[smaller]
    #   which is odd so the puzzle is unsolvable.


def PrintSolution(Solution):
    Path = []
    CurrentState = Solution
    while CurrentState:
        Path.append(CurrentState)
        CurrentState = CurrentState.Parent
    Path.reverse()  # Reverses the path to get the correct order from the initial state to the goal state.
    for Step in Path:
        print("Move:", Step.Move)
        PrintBoard(Step.Board)

  # This is the goal state of the puzzle which we need to get.
