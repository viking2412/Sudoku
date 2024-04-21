from ortools.sat.python import cp_model
from sys import stdin


def input_reader():
    grid = []
    constraints_lines = []
    for i, line in enumerate(stdin.readlines()):
        if i <= 10:
            line = line.strip().replace(" ", "").replace(".", "0")
            if line:
                grid.append([int(a) for a in line])
        else:
            constraints_lines.append(line)
    return grid, constraints_lines


def sudoku(mode, *args):
    if mode == "FILE":
        initial_grid, cons = input_reader()
    else:
        temp_grid, cons = args
        initial_grid = []
        for i in range(9):
            initial_grid.append([int(temp_grid[(i, j)]) for j in range(9)])
    model = cp_model.CpModel()
    model, line, grid = normal_sudoku_rules(model, initial_grid)
    if any(["T" in line for line in cons]):
        model = thermo(model, cons, grid)
    if any(["C" in line for line in cons]):
        model = killer_cage(model, cons, grid)
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    if status == cp_model.OPTIMAL:
        answer = []
        for i in line:
            answer.append([int(solver.value(grid[(i, j)])) for j in line])
    else:
        return "COULD NOT SOLVE"
    return answer


def normal_sudoku_rules(model: cp_model, initial_grid):
    cell_size = 3
    line_size = cell_size ** 2
    line = list(range(0, line_size))
    cell = list(range(0, cell_size))
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
    return model, line, grid


def thermo(model: cp_model, input_list, grid):
    for line in input_list:
        thermometers = []
        i = 1
        if "T" in line:
            while i+1 < len(line):
                thermometers.append((int(line[i])-1, int(line[i+1])-1))
                i += 2
            for i in range(len(thermometers)-1):
                x, y = thermometers[i]
                dx, dy = thermometers[i+1]
                model.add(grid[(x, y)] < grid[(dx, dy)])
    return model


def killer_cage(model: cp_model, input_list, grid):
    for line in input_list:
        cage = []
        i = 0
        if "C" in line:
            summ, indexes = int(line.partition(" ")[0][1:]), line.partition(" ")[2].strip()
            while i+1 < len(indexes):
                cage.append((int(indexes[i])-1, int(indexes[i+1])-1))
                i += 2
            model.add(sum([grid[(i, j)] for (i, j) in cage]) == summ)
            model.add_all_different(grid[(x, y)] for (x, y) in cage)
    return model


if __name__ == '__main__':
    sudoku("FILE")
