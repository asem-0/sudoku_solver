"""Sudoku Solver
This program solves a sudoku puzzle using recursion."""

from datetime import datetime as dt
from random import shuffle,randint,choice
import os
def board_loader(filename):
    """Loads a sudoku board from a file and returns a list of integers."""

    # Open the file and read the data
    with open(filename,"r") as f:
        data = f.readlines()
    
    # Create a list of integers from the data
    board_list = []
    for line in data:
        # Remove the newline character and split the line into a list
        board_list.extend(line.strip().split())
    # Convert the list of strings to a list of integers
    board_list = [int(i) for i in board_list]
    return board_list

class Board:
    """A class to represent a sudoku board."""
    def __init__(self,board = None) -> None:
        """Initializes the board object."""
        # Create a dictionary to represent the board
        self.board = {}
        
        # Fill the dictionary with the values from the board list
        counter_cells = 0   # Counter for the cells (since board is a flat list)
        # Iterate over the rows
        for row in range(9):
            # Iterate over the columns
            counter_col = 0
            for col in range(9):
                # If the board is not given, set the value to 0
                if not board:
                    value = 0
                # If the board is given, set the value to the value from the board list
                else:
                    value = board[counter_cells]
                
                # Add the value to the dictionary
                # The key is a string of the row, column, and block number {row}{col}{block}
                # The given formula ensures that the block number is unique for each block (1-9) 
                # starting from the top left block and moving right and down.
                # Example of a tile "121" -> row 1, column 2, block 1

                block = str(((counter_col//3)+1)+(counter_cells//27)*3)
                self.board.update({str(row+1)+str(col+1)+block:value})
                
                # Increment the counters
                counter_col += 1
                counter_cells += 1

        # Create a dictionary to store the tiles that fall within a row, column, or block (like a map)
        # This approach is faster than iterating over the board dictionary to find the tiles
        # that fall within a row, column, or block.
        self.rows = {
            "1":["111","121","131","142","152","162","173","183","193"],
            "2":["211","221","231","242","252","262","273","283","293"],
            "3":["311","321","331","342","352","362","373","383","393"],
            "4":["414","424","434","445","455","465","476","486","496"],
            "5":["514","524","534","545","555","565","576","586","596"],
            "6":["614","624","634","645","655","665","676","686","696"],
            "7":["717","727","737","748","758","768","779","789","799"],
            "8":["817","827","837","848","858","868","879","889","899"],
            "9":["917","927","937","948","958","968","979","989","999"],
        }
        self.cols={
            "1":["111","211","311","414","514","614","717","817","917"],
            "2":["121","221","321","424","524","624","727","827","927"],
            "3":["131","231","331","434","534","634","737","837","937"],
            "4":["142","242","342","445","545","645","748","848","948"],
            "5":["152","252","352","455","555","655","758","858","958"],
            "6":["162","262","362","465","565","665","768","868","968"],
            "7":["173","273","373","476","576","676","779","879","979"],
            "8":["183","283","383","486","586","686","789","889","989"],
            "9":["193","293","393","496","596","696","799","899","999"],
        }
        self.blocks={
            "1":["111","121","131","211","221","231","311","321","331"],
            "2":["142","152","162","242","252","262","342","352","362"],
            "3":["173","183","193","273","283","293","373","383","393"],
            "4":["414","424","434","514","524","534","614","624","634"],
            "5":["445","455","465","545","555","565","645","655","665"],
            "6":["476","486","496","576","586","596","676","686","696"],
            "7":["717","727","737","817","827","837","917","927","937"],
            "8":["748","758","768","848","858","868","948","958","968"],
            "9":["779","789","799","879","889","899","979","989","999"]
        }                
        # Create a list of the possible values for each tile
        # Eliminates the need to call the range function multiple times
        self.numset = range(1,10)

    def __str__(self) -> str:
        """Returns a string representation of the board that can be printed
        or saved to a file."""

        # Create a counter to keep track of the number of tiles
        count = 0
        # Create a string to store the board
        string = ""

        # Iterate over the tiles in the board
        for tile in self.board:
            # Add the value of the tile to the string
            string +=  str(self.board[tile]) + " "
            # Increment the counter
            count += 1
            # If the counter is divisible by 9, add a newline character (end of row)
            if count%9 == 0:
                # Remove the last space from the string
                string = string[:-1]
                # Add a newline character
                string += "\n"
        return string

    def get_empty_tiles(self):
        """Returns a list of the empty tiles on the board."""
        empty = []
        # Iterate over the tiles in the board
        for tile in self.board:
            # If the tile is empty, add it to the list
            if self.board[tile]==0:
                empty.append(tile)
        return empty
    
    def get_conflicts_index(self,tile):
        """Returns a list of the indexes of the tiles that conflict with the given tile, 
        as in they fall within the same row, column, or block."""
        conflicts_index =self.rows[tile[0]] + self.cols[tile[1]]+ self.blocks[tile[2]]
        return conflicts_index
    
    def get_conflicts_value(self,tile):
        """Returns a list of the values of the tiles that conflict with the given tile."""
        
        # Create a set to store the values of the conflicting tiles
        conflicts_value = set()
        
        # Iterate over the indexes of the conflicting tiles
        for index in self.get_conflicts_index(tile):
            # Add tile value to the list
            # Zeros are still added but it doesn't matter because they are not in the numset
            conflicts_value.add(self.board[index])
        
        # Return the list of conflicting values
        return list(conflicts_value)

    def get_possible_values(self,tile):
        """Returns a list of the possible values for the given tile."""

        # Get the values of the conflicting tiles
        conflicts = self.get_conflicts_value(tile)
        
        # The possible values are the values in the numset that are not in the conflicts list
        possible_values = set(self.numset) - set(conflicts)
        return possible_values
    
    def get_next_move(self):
        """Returns the next move to be made. The move is a list with the tile as the first element
        and the value as the second element. The tile is chosen by finding the tile with the least
        number of possible valid values."""

        # Create a list to store the possible moves
        moves = []
        # Iterate over the empty tiles
        for tile in self.get_empty_tiles():
            # Get the possible values for the tile
            allowed_moves = self.get_possible_values(tile)
            # If there are no possible values, return None (no solution)
            if len(allowed_moves)==0:
                return None
            # Otherwise, add the tile and its possible values to the list
            moves.append([tile,allowed_moves])

        # Pick the first move
        best_move = moves[0]
        # Iterate over the moves to find the move with the least number of possible values
        for current_move in moves[1:]:
            # If the move has only one possible value, return it (no need to search further)
            if len(best_move[1])==1:
                return best_move

            # If the current move in the loop has less possible values than the selected best move,
            # set the current move as the best move 
            if len(current_move[1])<len(best_move[1]):
                best_move = current_move
        # Return the best move, with the format [tile: [values]]
        return best_move


    def update_tile(self,move):
        """Updates the board with the given move. The move is a dictionary with the
        tile as the key."""
        # Looping is not necessary because there is only one key-value pair
        # but it is used to extract the value from the dictionary
        for tile,value in move.items():
            self.board[tile] = value
            return self.board
    
    def is_solved(self):
        """Returns True if the board is solved, False otherwise."""

        # If there is an empty tile, the board is not solved yet
        if 0 in self.board.values():
            return False
        
        # If there are no empty tiles, the board is solved
        return True
    
    def is_blocked(self):
        """Returns True if the board is blocked, False otherwise. A board is blocked if there
        are no empty tiles and there are no possible moves."""
        # Loop over the tiles in the board
        for tile in self.board:
            # If there is an empty tile, and there are possible moves, the board is not blocked
            if self.board[tile]==0:
                if len(self.get_possible_values(tile))!=0:
                    return False
        # Otherwise, the board is blocked
        return True

def random_board(filling_degree=1):
    """A function that creates a solvable sudoku board with a given filling degree.
    ### Filling degree
    is a number between 0 and 1 that indicates the percentage of filled tiles.
    1 means that all tiles are filled, 0 means that no tiles are filled."""
    
    # Holder for already filled tiles
    filled = []
    
    # Create a board
    board = Board()
    # Fill the board with 5 random values
    for i in range(5):
        # Choose a random tile
        tile = choice(list(board.board.keys()))

        # Make sure the tile is not already filled
        while tile in filled:
            # Choose a new tile
            tile = choice(list(board.board.keys()))
        
        # Add the tile to the filled list
        filled.append(tile)

        # Get the values in the row, col and block
        tile_values = [board.board[tile] for tile in board.rows[tile[0]]]
        tile_values += [board.board[tile] for tile in board.cols[tile[1]]]
        tile_values += [board.board[tile] for tile in board.blocks[tile[2]]]
        tile_values = set(tile_values)

        # Choose a random value
        value = randint(1,9)

        # Limit to prevent infinite loop
        limit = 0        

        # Make sure the value is not already in the row, col or block
        while value in tile_values:
            # Choose a new value
            value = randint(1,9)
            limit += 1
            if limit >= 100:
                return None
            
        board.update_tile({tile:value})
    
    # Solve the board
    board = solve_board(board)

    # If the board is not solved, return None
    if board is None:
        return None
    
    # calculate number of tiles to remove
    tiles_to_remove = 81 - int(81*filling_degree)

    # Removed tiles holder (to prevent removing the same tile twice)
    cleard_tiles = []

    # Remove tiles in a loop
    for i in range(tiles_to_remove):
        # Choose a random tile
        tile = choice(list(board.board.keys()))
        
        # Make sure the tile is not already removed
        while tile in cleard_tiles:
            tile = choice(list(board.board.keys()))
        
        # Add the tile to the removed tiles list
        cleard_tiles.append(tile)
        
        # Remove the tile (set value to 0)
        board.update_tile({tile:0})
    
    # Return the board after removing tiles
    return board

def create_solvable_board(filling_degree=1,filename=None):
    """A function that creates a solvable sudoku board with a given filling degree.
    and returns the board.

    ### Filling degree
    is a number between 0 and 1 that indicates the percentage of filled tiles.
    1 means that all tiles are filled, 0 means that no tiles are filled.
    ### Filename
    is the name of the file to save the board to. If no filename is given, 
    the board will not be saved.
    """
    # Create a variable to hold the board
    board = None
    # Start a loop to create a board
    # Loop stops when a valid board is created
    while board is None:
        # Create a board
        board = random_board(filling_degree)

    # If filename provided save the board to a file
    if filename is not None:
        with open(filename,"w") as f:
            f.write(str(board))

    return board

def solve_board(board):
    """A function that solves a sudoku board recursively.
    ###Board
    is a Board class object."""

    # If the board is solved, return the board
    if board.is_solved():
        return board
    
    # Get the best tile to fill with its possible values
    tile_move = board.get_next_move()

    # If no tile is found, return None (no solution)
    if tile_move is None:
        return None
    
    # Loop through the possible moves for the tile
    for move in tile_move[1]:
        # Create a copy of the board
        next_board = Board()
        next_board.board = board.board.copy()
        
        # Update the tile with the move
        next_board.update_tile({tile_move[0]:move})

        # Call the function again
        final_board = solve_board(next_board)

        # If the board is solved, return the board (solution)
        if final_board is not None:
            return final_board
    
    # If no solution is found, return None
    return None

def create_solution(puzzle_filename,solution_filename=None):
    """A function that solves a sudoku board and returns the solution board.
    if solution filename provided the solution is saved to a file.

    ### puzzle_filename
    is the name of the file containing the puzzle.
    ### solution_filename
    is the name of the file to save the solution to. If no filename is given,
    the solution will not be saved.
    """

    # Load the board from the file
    board = board_loader(puzzle_filename)
    # Create a board object
    start = Board(board)
    # Solve the board
    time_zero = dt.now()    # Start timer
    solution = solve_board(start)
    time_final = dt.now()   # Stop timer

    # If no solution is found, print message
    if solution is None:
        print(f"{puzzle_filename} - No solution")
    else:
        # Print the time taken to solve the board
        print(f"{puzzle_filename} - Time taken: {(time_final-time_zero).total_seconds():.3f} seconds")
        # If solution filename provided save the solution to a file
        if solution_filename is not None:
            with open(solution_filename,"w") as f:
                f.write(str(solution))
    
    # Return the solution
    return solution
