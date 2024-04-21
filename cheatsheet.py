from ortools.sat.python import cp_model


def solve_sudoku():
    """Solves the sudoku problem with the CP-SAT solver."""
    # Create the model.
    model = cp_model.CpModel()

    cell_size = 3
    line_size = cell_size**2
    line = list(range(0, line_size))
    cell = list(range(0, cell_size))

    initial_grid = [
        [0, 6, 0, 0, 5, 0, 0, 2, 0],
        [0, 0, 0, 3, 0, 0, 0, 9, 0],
        [7, 0, 0, 6, 0, 0, 0, 1, 0],
        [0, 0, 6, 0, 3, 0, 4, 0, 0],
        [0, 0, 4, 0, 7, 0, 1, 0, 0],
        [0, 0, 5, 0, 9, 0, 8, 0, 0],
        [0, 4, 0, 0, 0, 1, 0, 0, 6],
        [0, 3, 0, 0, 0, 8, 0, 0, 0],
        [0, 2, 0, 0, 4, 0, 0, 5, 0],
    ]

    grid = {}
    for i in line:
        for j in line:
            grid[(i, j)] = model.new_int_var(1, line_size, "grid %i %i" % (i, j))

    # AllDifferent on rows.
    for i in line:
        model.add_all_different(grid[(i, j)] for j in line)

    # AllDifferent on columns.
    for j in line:
        model.add_all_different(grid[(i, j)] for i in line)

    # AllDifferent on cells.
    for i in cell:
        for j in cell:
            one_cell = []
            for di in cell:
                for dj in cell:
                    one_cell.append(grid[(i * cell_size + di, j * cell_size + dj)])

            model.add_all_different(one_cell)

    # Initial values.
    for i in line:
        for j in line:
            if initial_grid[i][j]:
                model.add(grid[(i, j)] == initial_grid[i][j])

    # Solves and prints out the solution.
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    if status == cp_model.OPTIMAL:
        for i in line:
            print([int(solver.value(grid[(i, j)])) for j in line])


solve_sudoku()