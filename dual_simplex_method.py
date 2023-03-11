import numpy as np
from simplex_method import pivot_step

def can_be_improved_for_dual(tableau: np.ndarray) -> bool:
    """
    Takes a numpy tablea and returns whether it can be improved for the dual
    """
    rhs_entries = [row[-1] for row in tableau[:-1]]
    return any([entry < 0 for entry in rhs_entries])

def get_pivot_position_for_dual(tableau: np.ndarray) -> tuple[int, int]:
    """
    Uses the minimum ratio rule of the dual find the index of the  pivot
    returns a tuple where first element is the row, second element is the column
    """
    rhs_entries = [row[-1] for row in tableau[:-1]]
    min_rhs_value = min(rhs_entries)
    row = rhs_entries.index(min_rhs_value)
    columns = []
    for index, element in enumerate(tableau[row][:-1]):
        if element < 0:
            columns.append(index)
    columns_values = [tableau[-1][c] / tableau[row][c] for c in columns]
    column_min_index = columns_values.index(min(columns_values))
    column = columns[column_min_index]
    return row, column

def dual_simplex(tableau: np.ndarray, solve: bool = True) -> np.ndarray:
    """
    Performs the dual simplex algorithm and returns the solved tableau
    If solve is set to true it will solve the problem
    If it is set to false it will only perform one iteration
    """
    #tableau = to_tableau(c, A, b)

    if solve:
        while can_be_improved_for_dual(tableau):
            pivot_position = get_pivot_position_for_dual(tableau)
            tableau = pivot_step(tableau, pivot_position)
    elif can_be_improved_for_dual(tableau):
        pivot_position = get_pivot_position_for_dual(tableau)
        tableau = pivot_step(tableau, pivot_position)
                
    return np.array(tableau)