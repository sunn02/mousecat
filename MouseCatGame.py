import tkinter as tk
from PIL import Image, ImageTk

# Variables 
board_size = 7
board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
buttons = [[None for _ in range(board_size)] for _ in range(board_size)]
mouse_pos = (0, 0) 
cat_pos = (0, 3)    
turn = "mouse"  # Indica de quién es el turno
Max = "R"  # Representamos al ratón con 'R'
Min = "G"  # Representamos al gato con 'G'

# Inicializar Tkinter
root = tk.Tk()
root.geometry("180x180")
# Cargar imágenes
mouse_image_orig = Image.open("mouse.png")
cat_image_orig = Image.open("cat.png")
button_width = 60
button_height = 60
mouse_image = ImageTk.PhotoImage(mouse_image_orig.resize((35, 35)))
cat_image = ImageTk.PhotoImage(cat_image_orig.resize((35, 35)))

board[mouse_pos[0]][mouse_pos[1]] = Max
board[cat_pos[0]][cat_pos[1]] = Min

def update_buttons():
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == ' ':
                buttons[i][j].config(image='', text='', width=button_width, height=button_height)
            elif board[i][j] == Max:
                buttons[i][j].config(image=mouse_image, text='', width=button_width, height=button_height)
            elif board[i][j] == Min:
                buttons[i][j].config(image=cat_image, text='', width=button_width, height=button_height)

def create_board():
    for i in range(board_size):
        for j in range(board_size):
            button = tk.Button(root, width=5, height=5, command=lambda i=i, j=j: on_button_click(i, j))
            button.grid(row=i, column=j, sticky='nsew')
            buttons[i][j] = button

    for i in range(board_size):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i, weight=1)

def on_button_click(i, j):
    global turn, mouse_pos, cat_pos
    if turn == "mouse":
        if board[i][j] == ' ' and is_valid_move(mouse_pos, (i, j)):
            board[mouse_pos[0]][mouse_pos[1]] = ' '
            mouse_pos = (i, j)
            board[i][j] = Max
            update_buttons()  # Actualiza los botones después del movimiento del ratón

            if check_winner(mouse_pos, Max):
                show_winner(Max)
            else:
                turn = "cat"  # Cambia el turno al gato
                root.after(500, ai_move)  # Espera medio segundo antes del movimiento del gato

def ai_move():
    global turn, cat_pos
    # Primero, verifica si el gato puede moverse directamente al ratón
    for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_pos = (cat_pos[0] + move[0], cat_pos[1] + move[1])
        if new_pos == mouse_pos:
            board[cat_pos[0]][cat_pos[1]] = ' '
            cat_pos = new_pos
            board[cat_pos[0]][cat_pos[1]] = Min
            update_buttons()
            show_winner(Min)
            return

     # Si el gato no puede atrapar al ratón de inmediato, llamar a la función minimax
    move_val = minimax(board, True, 0)
    # Si el valor devuelto por minimax es mayor que -1 
    # (valor devuelto cuando no se puede atrapar al ratón), realiza el movimiento óptimo
    if move_val > -1:
        for action in get_actions(board, cat_pos):
            new_board = result(board, action, Min)
            if minimax(new_board, True, 0) == move_val:
                board[cat_pos[0]][cat_pos[1]] = ' '
                cat_pos = action
                board[cat_pos[0]][cat_pos[1]] = Min
                update_buttons()
                break

        if check_winner(cat_pos, Min):
            show_winner(Min)
        else:
            turn = "mouse"  # Cambia el turno al ratón

def is_valid_move(start, end):
    if abs(start[0] - end[0]) + abs(start[1] - end[1]) == 1:
        return True
    return False

def check_winner(pos, player):
    if player == Max and pos == (board_size - 1, board_size - 1): 
        return True
    if player == Min and pos == mouse_pos:
        return True
    return False

def show_winner(winner):
    for row in buttons:
        for button in row:
            button.config(state=tk.DISABLED)
    if winner == Max:
        print("El ratón ha escapado. ¡Gana el ratón!")
    else:
        print("El gato ha atrapado al ratón. ¡Gana el gato!")

def get_actions(board, pos):
    actions = []
    for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_pos = (pos[0] + move[0], pos[1] + move[1])
        if 0 <= new_pos[0] < board_size and 0 <= new_pos[1] < board_size and board[new_pos[0]][new_pos[1]] == ' ':  
            actions.append(new_pos)
    return actions

def result(board, action, player):
    new_board = [row[:] for row in board]
    new_board[action[0]][action[1]] = player
    return new_board

def minimax(board, max_turn, depth):
    if check_winner(mouse_pos, Max):
        return 1
    if check_winner(cat_pos, Min):
        return -1
    if depth >= 3:  # Limitar la profundidad a 3 niveles
        return 0

    if max_turn:
        max_value = float("-inf")
        for action in get_actions(board, mouse_pos):
            new_board = result(board, action, Max)
            value = minimax(new_board, False, depth + 1) #recursividad
            max_value = max(max_value, value)
        return max_value
    else:
        min_value = float("inf")
        for action in get_actions(board, cat_pos):
            new_board = result(board, action, Min)
            value = minimax(new_board, True, depth + 1)
            min_value = min(min_value, value)
        return min_value

# Configurar el tablero
create_board()
update_buttons()

# Ejecutar la interfaz
root.mainloop()



