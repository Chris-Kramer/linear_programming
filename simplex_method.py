import math
import numpy as np

def can_be_improved(tableau: np.ndarray) -> bool:
    """
    Test whether the current simplex tableau can be improved
    """
    z = tableau[-1]
    return any(x > 0 for x in z[:-1])

def get_pivot_position(tableau: np.ndarray) -> np.ndarray:
    """
    Uses the minimum ratio rule to find the index of the  pivot
    returns a tuple where first element is the row, second element is the column
    """
    z = tableau[-1]
    column = next(i for i, x in enumerate(z[:-1]) if x > 0)
    
    restrictions = []
    for eq in tableau[:-1]:
        el = eq[column]
        restrictions.append(math.inf if el <= 0 else eq[-1] / el)

    row = restrictions.index(min(restrictions))
    return row, column


def pivot_step(tableau: np.ndarray, pivot_position: tuple[int, int]) -> np.ndarray:
    """
    Performs a pivot based on the pivot position
    """
    new_tableau = [[] for eq in tableau]
    
    i, j = pivot_position
    pivot_value = tableau[i][j]
    new_tableau[i] = list(np.array(tableau[i]) / pivot_value)
    for eq_i, eq in enumerate(tableau):
        if eq_i != i:
            multiplier = list(np.array(new_tableau[i]) * tableau[eq_i][j])
            new_tableau[eq_i] = np.array(tableau[eq_i]) - multiplier
    return new_tableau

def is_basic(column: list[float | int]) -> bool:
    """
    Test if a column is basic, takes a list / np array as an input column
    """
    return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1

def get_solution(tableau: np.ndarray) -> np.ndarray:
    """
    Returns the solution vector of the current tableau
    """
    columns = np.array(tableau).T
    solutions = []
    for column in columns:
        solution = 0
        if is_basic(column):
            one_index = column.tolist().index(1)
            solution = columns[-1][one_index]
        solutions.append(solution)
    return np.array(solutions)


def simplex(tableau: np.ndarray, solve: bool = True) -> np.ndarray:
    """
    Performs the simplex algorithm on the supplied tableau
    if solve is set to false it will only perform one iteration
    """
    if solve:
        while can_be_improved(tableau):
            pivot_position = get_pivot_position(tableau)
            tableau = pivot_step(tableau, pivot_position)
    elif can_be_improved(tableau):
        pivot_position = get_pivot_position(tableau)
        tableau = pivot_step(tableau, pivot_position)
    
    return np.array(tableau)