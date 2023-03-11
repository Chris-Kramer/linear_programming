import numpy as np


def print_tbl(tableau: np.ndarray) -> None:
    """
    Prints a tableau to the console
    """
    print()
    display_tableau = np.array(tableau)
    for row_index, row in enumerate(display_tableau):
        for col, _ in enumerate(row):
            display_tableau[row_index, col] = round(display_tableau[row_index, col], 2)
    print(display_tableau)
    print()

def to_tableau(c: np.ndarray[float | int], A: np.ndarray[float | int], b: np.ndarray[float | int]):
    """
    Makes the vectors c, b and matrix A into a proper tableau
    """
    xb = [eq + [x] for eq, x in zip(A, b)]
    z = c + [0]
    return np.array(xb + [z])

#############################
# Matrix and list utilities #
#############################
def swap_list_elements(my_list: list, i: int, j: int):
    """
    Swap places of two elements in list
    """
    my_list[i], my_list[j] = my_list[j], my_list[i]

def swap_columns(my_array, i, j):
    """
    Swaps the columns of a numpy array
    """
    my_array[:, [i, j]] = my_array[:, [j, i]]

def swap_rows(my_array, i, j):
    """
    Swaps the rows of a numpy array
    """
    my_array[[i, j], :] = my_array[[j, i], :]