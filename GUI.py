import PySimpleGUI as sg
from main import sudoku


def sudoku_solver():
    layout_l = [[sg.Input(0, size=3, p=0, justification="center",
                          border_width=1, key=(i, j)) for j in range(9)] for i in range(9)]

    layout_r = [[sg.Button("Solve")]]

    layout = [[sg.Col(layout_l, p=0), sg.Col(layout_r, p=0)]]

    window = sg.Window('Sudoku Solver', layout)
    temp_storage = {}
    first_launch = True
    while True:
        event, values = window.read()
        cons = ""
        print(values)
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == "Solve":
            for i in range(9):
                for j in range(9):
                    temp_storage[(i, j)] = values[(i, j)]
            solved = sudoku("GUI", values, cons)
            if type(solved) == str:
                sg.popup_ok(solved)
                continue
            else:
                solved_layout = [[sg.Input(solved[i][j], size=3, p=0, justification="center",
                                           border_width=1, key=("s", i, j)) for j in range(9)] for i in range(9)]

                layout_l = [[sg.Input(temp_storage[(i, j)], size=3, p=0, justification="center",
                                      border_width=1, key=(i, j)) for j in range(9)] for i in range(9)]

                layout_c = [[sg.Button("Solve")],
                            [sg.Button("Reset Values")]]
                layout = [[sg.Col(layout_l), sg.Col(layout_c), sg.Col(solved_layout)]]
            if first_launch:
                window.close()
                window = sg.Window('Sudoku Solver', layout)
                first_launch = False
                window.read()
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
            for i in range(9):
                for j in range(9):
                    window[(i, j)].update(temp_storage[(i, j)])
                    window[("s", i, j)].update(solved[i][j])
            if event == "Reset Values":
                for i in range(9):
                    for j in range(9):
                        window[(i, j)].update(0)
    window.close()


if __name__ == '__main__':
    sudoku_solver()
