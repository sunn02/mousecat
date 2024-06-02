import tkinter as tk

class MouseCatGame:
    def __init__(self, root):
        self.root = root
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.Max = "R"  # Representamos al ratón con 'R'
        self.Min = "G"   # Representamos al gato con 'G'
        self.mouse_pos = (0, 0)  # El ratón comienza en la esquina superior izquierda
        self.cat_pos = (2, 2)    # El gato comienza en la esquina inferior derecha
        self.board[self.mouse_pos[0]][self.mouse_pos[1]] = self.Max
        self.board[self.cat_pos[0]][self.cat_pos[1]] = self.Min
        
        self.mouse_image = tk.PhotoImage(file="mouse.png")
        self.cat_image = tk.PhotoImage(file="cat.png")
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=self.board[i][j], font='Arial 20', width=5, height=2,
                                   command=lambda i=i, j=j: self.on_button_click(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def on_button_click(self, i, j):
        if self.board[i][j] == ' ' and self.is_valid_move(self.mouse_pos, (i, j)):
            self.board[self.mouse_pos[0]][self.mouse_pos[1]] = ' '
            self.mouse_pos = (i, j)
            self.board[i][j] = self.Max
            self.update_buttons()  # Actualiza los botones después del movimiento del ratón

            if self.check_winner(self.mouse_pos, self.Max):
                self.show_winner(self.Max)
                return

            self.mouse_turn = False
            self.root.after(100, self.ai_move)  # Mover el gato inmediatamente después del ratón

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
            self.board[self.cat_pos[0]][self.cat_pos[1]] = self.Min
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
                min_value = min(min_value, value)
            return min_value

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i][j])

if __name__ == "__main__":
    root = tk.Tk()
    game = MouseCatGame(root)
    root.mainloop()

