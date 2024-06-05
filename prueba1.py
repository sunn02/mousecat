

class MouseCat:
    def __init__(self):
        self.Max = "R"
        self.Min = "G"
        self.tablero = [[' ' for _ in range(3)] for _ in range(3)]
        self.mouse_pos = (0,0)
        self.cat_pos = (2,2)
        self.tablero[self.mouse_pos[0]]

    def mostrar_tablero(self):
        for fila in self.tablero:
            print("|".join(fila))
            print("-"*5)

    def minimax(self, winner, max_turn):
        if winner == self.Max:
            return 1
        if winner == self.Min:
            return -1
        
        if max_turn:
            max_value = float("-inf")
        pass

        
tablero = MouseCat()
tablero.mostrar_tablero()

    