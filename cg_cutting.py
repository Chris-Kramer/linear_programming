# Imports #
###########
import numpy as np
from math import floor
from simplex_method import get_solution, simplex
from dual_simplex_method import dual_simplex
from utils import swap_columns, swap_list_elements, swap_rows


#####################
# Specific LP utils #
#####################
def _fractional_part(number: float | int) -> float:
    """
    Returns the fractional part of a number
    """
    return number - floor(number)
                  
def _scaled_fractional_part(number: float | int) -> int:
    """
    Scales the fraction, this is usefull to avoid python rounding errors
    """
    return int(floor((number - floor(number)) * 1000))

def _select_row(tableau):
    """
    Returns the index of the first row, which contains a fraction
    """
    for row in range(len(tableau) - 1):
        if _scaled_fractional_part(tableau[row, -1]) != 0 and not _scaled_fractional_part(tableau[row, -1]) > 997:
            selected_row = row
            break
    return selected_row

def _get_gomory_constraint(tableau: np.ndarray, selected_row: int):
    """
    Returns the gomory constraint of the selected row as a list
    """
    row = tableau[selected_row]
    gomory_constraint = []
    for val in row:
        fraction = _fractional_part(val)
        if fraction != 0:
            gomory_constraint.append(-fraction)
        else: 
            gomory_constraint.append(0)
    return gomory_constraint

def _add_gomory_constraint_to_tableau(tableau: np.ndarray, gomory_constraint: list[float]) -> np.ndarray:
    """
    Adds the gomory constraint the tableau with a new slack variable
    """
    # Add slack variable to constraint
    gomory_constraint.append(1)

    # Add column for slack variabel to tableau
    zero_col = np.array([[0] for i in range(len(tableau))])
    tableau = np.append(tableau, zero_col, axis=1)
    tableau = np.vstack([tableau, gomory_constraint])

    # Swap the elements around so the columns and rows are arranged like the original tableau
    swap_list_elements(gomory_constraint, -1, -2)
    swap_columns(tableau, -1, -2)
    swap_rows(tableau, -1, -2)
    
    return tableau

def cg_cut(tableau: np.ndarray) -> np.ndarray:
    """
    Adds one CG-cut to the array
    """
    gomory_constraint = _get_gomory_constraint(tableau, selected_row = _select_row(tableau))
    return _add_gomory_constraint_to_tableau(tableau, gomory_constraint)


def contains_non_integers(tableau: np.ndarray, decision_vars: list[int]) -> bool:
    """
    Test if a solution contains non integers
    The list of decision variables is the second parameter
    It refers to the column indeces of the decision variables
    """
    solutions = get_solution(tableau)
    for decision_var in decision_vars:
        decision_sol = solutions[decision_var]
        if _scaled_fractional_part(decision_sol) != 0 or not _scaled_fractional_part(decision_sol) > 997:
            return True
    return False

########################
# Full public function #
########################
def cg_cutting_planes(tableau: np.ndarray, decision_vars: list[int]) -> np.ndarray:
    """
    Performs the chvatal-gomory cutting plane algorithm to the supplied tableau
    Returns the final tableau 
    """
    solved_tableau = np.array(simplex(tableau))
    while contains_non_integers(solved_tableau, decision_vars):
        try: 
            solved_tableau = cg_cut(solved_tableau)
            solved_tableau = np.array(dual_simplex(solved_tableau, solve = False))
        except (ValueError, UnboundLocalError):
            return solved_tableau
    return solved_tableau
