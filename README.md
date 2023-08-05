# Sudoku_solver
## Introduction
By: Asem Al-Shaibani \
05.08.2023
#### Description:
A simple module that solves and creates Sudoku games.
#### Video Demo:

## Usage
The functions in Sudoku can be imported and used as part of another script.
### Example:
#### Create puzzles
To create a puzzle import the create_solvable_board function
```
from sudoku_solver_opt import create_solveable_board
```
The function returns the puzzle board with Board class and it can also write the puzzle to a file if the filename is specified in the call
```
solvable_ board = create_solveable_board(filling_degree,filename)
```
where *filling_degree* is a parameter between 0 and 1 that specifies the percentage of the filled tiles in the board. 1 will return a fully solved board
while 0 will return an empty board. 
and *filename* is the output filename of the puzzle. 

#### Solve a puzzle
Import the create_solution function
```
from sudoku_solver_opt import create_solution
```

Similar to creating puzzles, the function returns the solved board is possible and will also write the solution to a file if filename is provided.
```
solution = create_solution(puzzle_filename,solution_filename)
```
where *puzzle_filename* is the filename of the puzzle to be solved, and *solution_filename* is an optional parameter for the filename of the solution.

### Puzzle format
The puzzle file for input is a basic txt file with 9 rows representing the rows of the Sudoku puzzle, the values are separated by spaces as follows:
```
2 5 6 8 4 7 9 1 3
3 8 4 9 1 5 6 2 7
1 9 7 2 3 6 4 8 5
4 2 1 3 9 8 5 7 6
9 6 8 7 5 1 3 4 2
5 7 3 4 6 2 8 9 1
6 3 9 1 2 4 7 5 8
8 4 2 5 7 3 1 6 9
7 1 5 6 8 9 2 3 4
```

## Technical aspects
The internal representation of the board depends on a dict object with strings as keys. The key represent the location of the tile on the board. Example "142" is the tile at the first row, fourth column, and second block. In this case an impossible tile is "141" since the fourth column must be in block 2, 5, or 8 not in block 1. 

The blocks start from the top left and go to the right and down.

The algorithm finds the tile with the least number of possible moves and starts there. This reduces the number of possible trees to be explored and makes it faster to find the solution

### Limitations
The algorithm to generate puzzles does not ensure that there is only a single unqiue solution which means that at lower filling degrees the function might 
produce puzzles with multiple solutions. 

Similarily the solver function will only return the first solution if multiple solutions are possible. 

 

## Licence
This module is given under MIT license.
