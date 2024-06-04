import tkinter as tk
from PIL import Image, ImageTk

class MouseCatGame:
    def __init__(self, root):
        self.root = root
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.Max = "R"  # Representamos al ratón con 'R'
        self.Min = "G"  # Representamos al gato con 'G'
        self.mouse_pos = (0, 0)  # El ratón comienza en la esquina superior izquierda
        self.cat_pos = (2, 2)  # El gato comienza en la esquina inferior derecha

        # Cargar imágenes
        self.mouse_image_orig = Image.open("mouse.png")
        self.cat_image_orig = Image.open("cat.png")

        # Crear el tablero y luego ajustar el tamaño de las imágenes
        self.create_board()
        self.adjust_images()
        self.update_buttons()

        # Ajustar el tamaño de la ventana para que se vea todo el tablero
        self.root.geometry("180x180")  # Ajusta según el tamaño del tablero y los botones

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, width=5, height=5, command=lambda i=i, j=j: self.on_button_click(i, j))
                button.grid(row=i, column=j, sticky='nsew')
                self.buttons[i][j] = button

        # Ajustar las filas y columnas para que tengan el mismo tamaño
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def adjust_images(self):
        button_size = 60  # Ajusta el tamaño del botón

        # Redimensionar las imágenes al tamaño de los botones
        self.mouse_image = ImageTk.PhotoImage(self.mouse_image_orig.resize((button_size, button_size), Image.LANCZOS))
        self.cat_image = ImageTk.PhotoImage(self.cat_image_orig.resize((button_size, button_size), Image.LANCZOS))

        self.board[self.mouse_pos[0]][self.mouse_pos[1]] = self.mouse_image
        self.board[self.cat_pos[0]][self.cat_pos[1]] = self.cat_image

    def on_button_click(self, i, j):
        if self.board[i][j] == ' ' and self.is_valid_move(self.mouse_pos, (i, j)):
            self.board[self.mouse_pos[0]][self.mouse_pos[1]] = ' '
            self.mouse_pos = (i, j)
            self.board[i][j] = self.mouse_image
            self.update_buttons()  # Actualiza los botones después del movimiento del ratón

            if self.check_winner(self.mouse_pos, self.Max):
                self.show_winner(self.Max)

            self.mouse_turn = False
            self.root.after(10, self.ai_move)  # Reducir el retraso al mínimo

    def ai_move(self):
        best_val = float("inf")
        best_move = None
        for action in self.get_actions(self.board, self.cat_pos):
            new_board = self.result(self.board, action, self.Min)
            move_val = self.minimax(new_board, True)
            if move_val < best_val:
                best_val = move_val
                best_move = action
        if best_move:
            self.board[self.cat_pos[0]][self.cat_pos[1]] = ' '
            self.cat_pos = best_move
            self.board[self.cat_pos[0]][self.cat_pos[1]] = self.cat_image
            self.update_buttons()

            if self.check_winner(self.cat_pos, self.Min):
                self.show_winner(self.Min)

    def is_valid_move(self, start, end):
        # Verificar si el movimiento es adyacente (arriba, abajo, izquierda, derecha)
        if abs(start[0] - end[0]) + abs(start[1] - end[1]) == 1:
            return True
        return False

    def check_winner(self, pos, player):
        if player == self.Max and pos == (2, 2):
            return True
        if player == self.Min and pos == self.mouse_pos:
            return True
        return False

    def show_winner(self, winner):
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)
        if winner == self.Max:
            print("El ratón ha escapado. ¡Gana el ratón!")
        else:
            print("El gato ha atrapado al ratón. ¡Gana el gato!")

    def get_actions(self, board, pos):
        actions = []
        for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            if 0 <= new_pos[0] < 3 and 0 <= new_pos[1] < 3 and board[new_pos[0]][new_pos[1]] == ' ':
                actions.append(new_pos)
        return actions

    def result(self, board, action, player):
        new_board = [row[:] for row in board]
        new_board[action[0]][action[1]] = player
        return new_board

    def minimax(self, board, max_turn):
        if self.check_winner(self.mouse_pos, self.Max):
            return 1
        if self.check_winner(self.cat_pos, self.Min):
            return -1

        if max_turn:
            max_value = float("-inf")
            for action in self.get_actions(board, self.mouse_pos):
                new_board = self.result(board, action, self.Max)
                value = self.minimax(new_board, False)
                max_value = max(max_value, value)
            return max_value
        else:
            min_value = float("inf")
            for action in self.get_actions(board, self.cat_pos):
                new_board = self.result(board, action, self.Min)
                value = self.minimax(new_board, True)
                # Agregamos la heurística para minimizar la distancia entre el gato y el ratón
                distance = abs(action[0] - self.mouse_pos[0]) + abs(action[1] - self.mouse_pos[1])
                value -= distance
                min_value = min(min_value, value)
            return min_value

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.buttons[i][j].config(image='', text='', width=60, height=60)
                else:
                    self.buttons[i][j].config(image=self.board[i][j], text='', width=60, height=60)

if __name__ == "__main__":
    root = tk.Tk()
    game = MouseCatGame(root)
    root.mainloop()









