from ..algorithm.algorithm import Algorithm

def model_algorithm(letters, board):
    algorithm = Algorithm(letters,board)
    return algorithm.algorithm_engine()