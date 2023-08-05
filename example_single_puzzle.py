from sudoku_solver_opt import create_solvable_board, create_solution

filling_degree = 0.5
board = create_solvable_board(filling_degree,".//puzzle_x.txt")
solution = create_solution(".//puzzle_x.txt",".//puzzle_x_solution.txt")