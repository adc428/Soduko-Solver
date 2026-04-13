
# Project: Sudoku Solver and Generator

# Description

This project implements a Sudoku solver and random board generator in Python.  
The program represents Sudoku boards as 9x9 lists and uses rule-based logic to determine valid moves, solve cells with a single legal value, and detect invalid or unsolvable boards.  
If the board reaches a point where multiple valid moves are possible, the user can continue the solving process by selecting one of the legal options.

# Components

Options Engine (`options`):
Returns all valid digits for a selected empty cell.

Possibility Matrix Builder (`possible_digits`):
Creates a full matrix of candidate values for every board position.

Stage Solver (`one_stage`):
Executes one solving stage by filling forced cells and updating all related candidates.

Board Filler (`fill_board`):
Runs the full solving flow until success, failure, or user decision is needed.

Random Board Creator (`create_random_board`):
Generates a random initial Sudoku board with legal values.

Board Display and File Export:
Includes formatted console printing and output file writing for results.

# Features

Automatic Sudoku validation.

Detection of illegal and unsolvable boards.

Rule-based solving using candidate elimination.

Interactive solving for ambiguous cases.

Random legal board generation.

Formatted board printing to console and file.

# Requirements

Python 3.x

No external libraries required.

# Output

Results are saved to `sudoku_solved.txt`, including solved boards and status messages.
