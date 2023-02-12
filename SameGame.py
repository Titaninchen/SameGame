import random
import tkinter as tk
import functools


# possible settings
field_height = 10
field_length = 10
colour_variation = 6


# building play field
field = [[0 for x in range(field_length)] for y in range(field_height)]

for i in range(field_height):
    for j in range(field_length):
        field[i][j] = random.randint(1, colour_variation)


# Standard Variables
removed_buttons_list = set()
buttons = [[None for x in range(field_length)] for y in range(field_height)]
count_moves = 0
remaining_stones = field_height * field_length


# colors
colors = {
    0: "white",
    1: "red",
    2: "green",
    3: "blue",
    4: "pink",
    5: "orange",
    6: "violet",
    7: "brown",
    8: "yellow",
    9: "turquoise"
}


# Layout
root = tk.Tk()
buttons = []


# Event Button Click
def button_click(button, row, col):
    global count_moves
    count_moves = count_moves + 1
    print("starting move number", count_moves, "\n")
    if field[row][col] == 0:
        print("not allowed to click on white row", row, "col", col, "\n\nfinished move", count_moves, "with", remaining_stones, "remaining stones\n\n----------\n")
        return
    check_button(button, row, col)
    check_near_button(button, row, col)
    remove_button(button, row, col)
    fall_down()
    moving_left()
    print("finished move", count_moves, "with", remaining_stones, "remaining stones\n\n----------\n")


# Check stone remove
def check_button(button, row, col):
    global removed_buttons_list, buttons
    if buttons[row][col] in removed_buttons_list:
        return

    color = field[row][col]

    # Check if adjacent buttons have the same color = legitimate move
    if row > 0 and field[row - 1][col] == color:
        removed_buttons_list.add(button)
        return
    if row < field_height - 1 and field[row + 1][col] == color:
        removed_buttons_list.add(button)
        return
    if col > 0 and field[row][col - 1] == color:
        removed_buttons_list.add(button)
        return
    if col < field_length - 1 and field[row][col + 1] == color:
        removed_buttons_list.add(button)
        return
    else:
        print("no stones with the same color nearby row", row, "col", col)


    # Check near Stones
def check_near_button(button, row, col):
    global removed_buttons_list, buttons
    if len(removed_buttons_list) == 0:
        return

    color = field[row][col]

    if row > 0 and field[row - 1][col] == color:
        if buttons[row - 1][col] not in removed_buttons_list:
            removed_buttons_list.add(buttons[row - 1][col])
            check_near_button(buttons[row - 1][col], row - 1, col)

    if row < field_height - 1 and field[row + 1][col] == color:
        if buttons[row + 1][col] not in removed_buttons_list:
            removed_buttons_list.add(buttons[row + 1][col])
            check_near_button(buttons[row + 1][col], row + 1, col)

    if col > 0 and field[row][col - 1] == color:
        if buttons[row][col - 1] not in removed_buttons_list:
            removed_buttons_list.add(buttons[row][col - 1])
            check_near_button(buttons[row][col - 1], row, col - 1)

    if col < field_length - 1 and field[row][col + 1] == color:
        if buttons[row][col + 1] not in removed_buttons_list:
            removed_buttons_list.add(buttons[row][col + 1])
            check_near_button(buttons[row][col + 1], row, col + 1)


# Remove all removeble buttons
def remove_button(button, row, col):
    global removed_buttons_list, buttons, remaining_stones
    for col in range(field_length):
        for row in range(field_height):
            if buttons[row][col] in removed_buttons_list:
                field[row][col] = 0
                buttons[row][col].config(bg=colors[0])
                removed_buttons_list.remove(buttons[row][col])
                print("removed_stone on row", row, "col", col)
                remaining_stones =  remaining_stones - 1
                remove_button(button, row, col)
                return
    print("removing_finished\n")


# Check if a stone can fall down
def fall_down():
    global field, buttons, colors
    # Check if the stone can fall down
    for col in range(field_length):
        for row in range(field_height):
            if field[row][col] == 0:
                if row > 0 and field[row - 1][col] != 0:
                    # Move the stone down row
                    print("moving Stone from row", row - 1, "col", col, "to row", row, "col", col)
                    field[row][col] = field[row - 1][col]
                    field[row - 1][col] = 0
                    # Update the grid location of the button in the buttons list
                    buttons[row][col].config(bg=str(colors[field[row][col]]))
                    buttons[row - 1][col].config(bg=str(colors[field[row - 1][col]]))
                    fall_down()
                    return
    print("moving Stones down finished\n")


# checking if a column can move left
def moving_left():
    global field, buttons, colors
    for col in range(field_length):
        if field[field_height - 1][col] == 0:
            if col + 1 < field_length and field[field_height - 1][col + 1] != 0:
                # Move the col left
                print("moving column from column", col + 1, "to column", col)
                for row in range (field_height):
                    field[row][col] = field[row][col + 1]
                    field[row][col + 1] = 0
                    # Update the grid location of the button in the buttons list
                    buttons[row][col].config(bg=str(colors[field[row][col]]))
                    buttons[row][col + 1].config(bg=str(colors[field[row][col + 1]]))
                moving_left()
                return
    print("moving column left finished\n")


def setup_gameplay():
    global all
    for i in range(field_height):
        row = []
        for j in range(field_length):
            button = tk.Button(root, bg=str(colors[field[i][j]]), width=10, height=5)
            button.grid(row=i, column=j, padx=1, pady=1)
            button.config(command=functools.partial(button_click, button, i, j))
            row.append(button)
        buttons.append(row)


setup_gameplay()
root.mainloop()