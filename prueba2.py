import tkinter as tk

class tic():
    def __init__(self, root):
        self.root = root 
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.Max = "Raton"
        self.Min = "Gato"
        
        
    def terminal_state(self, winner):
        if winner == self.Max:
            return 1 
        elif winner == self.Min:
            return -1
        else:
            return 0 
        
        
    def get_actions(self): #Devuelve una lista de todas las posiciones vacias en el tablero
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' '] 
    
    def result(self, board, action, player):
        new_board = [row[:] for row in board]
        new_board[action[0]][action[1]] = player
        return new_board
        
    
    def minimax(self, board, max_turn):
        if max_turn:
            max_value = float("-inf")
            for action in self.get_actions():
                new_board = self.result(board, action, self.Max)
                value = self.minimax(new_board, False)  # Cambiar a False para el jugador Min
                max_value = max(max_value, value)
            return max_value 
        
        else:
            min_value = float("inf")
            for action in self.get_actions():
                new_board = self.result(board, action, self.Min)
                value = self.minimax(new_board, True) # Cambiar a True para el jugador Max
                min_value = min(min_value, value) 
            return min_value 
        
        
if __name__ == "__main__":
    root = tk.Tk()
    root.mainloop()