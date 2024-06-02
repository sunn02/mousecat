import tkinter as tk

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.Max = "Raton"
        self.Min = "Gato"
        self.current_player = self.Max  # Humano empieza
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=' ', font='Arial 20', width=5, height=2,
                                   command=lambda i=i, j=j: self.on_button_click(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def on_button_click(self, i, j):
        if self.board[i][j] == ' ' and self.current_player == self.Max:
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player)
            if self.check_winner(self.board, self.current_player):
                self.show_winner(self.current_player)
                return
            elif not self.get_actions(self.board):
                self.show_winner(None)  # Empate
                return
            self.current_player = self.Min
            self.root.after(500, self.ai_move)  # Esperar 500ms antes del movimiento de la IA

    def ai_move(self):
        best_val = float("inf")
        best_move = None
        for action in self.get_actions(self.board):
            new_board = self.result(self.board, action, self.Min)
            move_val = self.minimax(new_board, True)
            if move_val < best_val:
                best_val = move_val
                best_move = action
        if best_move:
            self.board[best_move[0]][best_move[1]] = self.Min
            self.buttons[best_move[0]][best_move[1]].config(text=self.Min)
            if self.check_winner(self.board, self.Min):
                self.show_winner(self.Min)
                return
            elif not self.get_actions(self.board):
                self.show_winner(None)  # Empate
                return
            self.current_player = self.Max

    def terminal_state(self, board, winner):
        if winner == self.Max:
            return 1
        elif winner == self.Min:
            return -1
        else:
            return 0

    def get_actions(self, board):
        return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

    def result(self, board, action, player):
        new_board = [row[:] for row in board]
        new_board[action[0]][action[1]] = player
        return new_board

    def minimax(self, board, max_turn):
        if self.check_winner(board, self.Max):
            return 1
        elif self.check_winner(board, self.Min):
            return -1
        elif not self.get_actions(board):  # Si no hay más acciones, es un empate
            return 0

        if max_turn:
            max_value = float("-inf")
            for action in self.get_actions(board):
                new_board = self.result(board, action, self.Max)
                value = self.minimax(new_board, False)
                max_value = max(max_value, value)
            return max_value
        else:
            min_value = float("inf")
            for action in self.get_actions(board):
                new_board = self.result(board, action, self.Min)
                value = self.minimax(new_board, True)
                min_value = min(min_value, value)
            return min_value

    def check_winner(self, board, player):
        # Check rows, columns and diagonals for a win
        for i in range(3):
            if all([board[i][j] == player for j in range(3)]) or all([board[j][i] == player for j in range(3)]):
                return True
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return True
        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return True
        return False

    def show_winner(self, winner):
        if winner:
            win_text = f"¡{winner} gana!"
        else:
            win_text = "¡Es un empate!"
        win_label = tk.Label(self.root, text=win_text, font='Arial 20')
        win_label.grid(row=3, column=0, columnspan=3)
        self.disable_buttons()

    def disable_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()


