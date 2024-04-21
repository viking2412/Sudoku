import PySimpleGUI as sg

headings = ['First Name', 'Last Name', 'Age']
data = [
    ['John', 'Smith', 39],
    ['Mary', 'Jane', 25],
    ['Jennifer', 'Doe', 28],
]
modes = (sg.TABLE_SELECT_MODE_NONE, sg.TABLE_SELECT_MODE_BROWSE, sg.TABLE_SELECT_MODE_EXTENDED)
mode = sg.TABLE_SELECT_MODE_EXTENDED

sg.theme('LightBlue')
layout = [
    [[sg.Input(0, size=3, justification="center") for _ in range(9)] for _ in range(9)]
]

window = sg.Window("Title", layout)

while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event in modes:
        mode = event
        window['-TABLE-'].widget.configure(select=mode)

window.close()

# [sg.Table(values=data,
                #           max_col_width=25,
                #           auto_size_columns=True,
                #           justification='center',
                #           num_rows=20,
                #           alternating_row_color=sg.theme_button_color()[1],
                #           key='-TABLE-',
                #           expand_x=True,
                #           expand_y=True,
                #           enable_click_events=True)],