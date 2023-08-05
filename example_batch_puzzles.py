import os
from sudoku_solver_opt import create_solvable_board, create_solution,random_board

# How many puzzles to generate
limit = 10

filling_degree = 0.4

for i in range(limit+1):
    board = create_solvable_board(filling_degree,f".//generated_puzzles//puzzle_{i:04d}.txt")
    print(f"Board {i} generated")        


for file in os.listdir(".//generated_puzzles//"):
    solution = create_solution(f".//generated_puzzles//{file}",f".//generated_solutions//solution_{file}")
