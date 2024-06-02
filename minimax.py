# terminal = true or false 
# value of terminal state = 1 or -1
# player = max or min
# actions = izq, derecha, ect
# result

# if terminal: (terminal state, game over)
# return value (result, who won)

# if max player (turn)
# value = -infinite (desde lo chico a lo mas grande)
# for a in Actions:
# value = Mac(value, Minimax(Result))
# return value

# if min
# value=infinity
# for a in actions
# value = Min(value, Minimax(Result))
# return value

import tkinter as tk
from collections import deque

# Constantes
HOLE = 0
MOUSE_START = 1
CAT_START = 2
MOUSE_TURN = 0
CAT_TURN = 1
MOUSE_WIN = 1
CAT_WIN = 2
DRAW = 0
SAFE_ZONE = [6, 18]  # Ejemplo de casillas de escape seguras

class CatMouseGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Cat and Mouse Game")
        self.canvas = tk.Canvas(self.master, width=600, height=600)
        self.canvas.pack()
        self.board_size = 5
        self.cell_size = 600 // self.board_size
        self.graph = self.create_graph(self.board_size)
        self.setup_game()
        self.canvas.bind_all("<KeyPress>", self.key_press)
        self.update_board()

    def create_graph(self, size):
        graph = []
        for i in range(size):
            for j in range(size):
                neighbors = []
                if i > 0: neighbors.append((i - 1) * size + j)  # Up
                if i < size - 1: neighbors.append((i + 1) * size + j)  # Down
                if j > 0: neighbors.append(i * size + j - 1)  # Left
                if j < size - 1: neighbors.append(i * size + j + 1)  # Right
                graph.append(neighbors)
        return graph

    def setup_game(self):
        self.mouse_pos = 0
        self.cat_pos = self.board_size**2 - 1
        self.turn = MOUSE_TURN
        self.result = self.cat_mouse_game()

    def key_press(self, event):
        if self.turn == MOUSE_TURN:
            if event.keysym == 'Up':
                self.move_mouse(-self.board_size)
            elif event.keysym == 'Down':
                self.move_mouse(self.board_size)
            elif event.keysym == 'Left':
                self.move_mouse(-1)
            elif event.keysym == 'Right':
                self.move_mouse(1)
        self.update_board()
        if self.turn == CAT_TURN:
            self.cat_move()
            self.update_board()

    def move_mouse(self, move):
        new_pos = (self.mouse_pos + move) % (self.board_size**2)
        if new_pos in self.graph[self.mouse_pos]:
            self.mouse_pos = new_pos
            if self.mouse_pos in SAFE_ZONE:
                print("¡El ratón ha ganado!")
                self.master.destroy()
            else:
                self.turn = CAT_TURN if self.turn == MOUSE_TURN else MOUSE_TURN

    def cat_move(self):
        # Lógica simple para mover el gato hacia el ratón
        mouse_x, mouse_y = self.mouse_pos % self.board_size, self.mouse_pos // self.board_size
        cat_x, cat_y = self.cat_pos % self.board_size, self.cat_pos // self.board_size
        if cat_x < mouse_x:
            self.cat_pos += 1
        elif cat_x > mouse_x:
            self.cat_pos -= 1
        elif cat_y < mouse_y:
            self.cat_pos += self.board_size
        elif cat_y > mouse_y:
            self.cat_pos -= self.board_size
        if self.cat_pos == self.mouse_pos:
            print("¡El gato ha ganado!")
            self.master.destroy()
        else:
            self.turn = MOUSE_TURN

    def update_board(self):
        if not self.canvas.winfo_exists():
            return
        self.canvas.delete("all")
        for i in range(self.board_size):
            for j in range(self.board_size):
                x0 = i * self.cell_size
                y0 = j * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                color = "green" if (i * self.board_size + j) in SAFE_ZONE else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        mx, my = (self.mouse_pos % self.board_size) * self.cell_size, (self.mouse_pos // self.board_size) * self.cell_size
        self.canvas.create_oval(mx, my, mx + self.cell_size, my + self.cell_size, fill="blue")
        cx, cy = (self.cat_pos % self.board_size) * self.cell_size, (self.cat_pos // self.board_size) * self.cell_size
        self.canvas.create_oval(cx, cy, cx + self.cell_size, cy + self.cell_size, fill="red")

    def cat_mouse_game(self):
        nodes_count = len(self.graph)
        result = [[[DRAW] * 2 for _ in range(nodes_count)] for _ in range(nodes_count)]
        degrees = [[[0] * 2 for _ in range(nodes_count)] for _ in range(nodes_count)]
        
        for mouse_pos in range(nodes_count):
            for cat_pos in range(1, nodes_count):
                degrees[mouse_pos][cat_pos][MOUSE_TURN] = len(self.graph[mouse_pos])
                degrees[mouse_pos][cat_pos][CAT_TURN] = len(self.graph[cat_pos]) - self.graph[cat_pos].count(HOLE)

        def get_prev_states(mouse_pos, cat_pos, turn):
            previous_states = []
            prev_turn = 1 - turn
            if prev_turn == CAT_TURN:
                for prev_cat_pos in self.graph[cat_pos]:
                    if prev_cat_pos != HOLE:
                        previous_states.append((mouse_pos, prev_cat_pos, prev_turn))
            else:
                for prev_mouse_pos in self.graph[mouse_pos]:
                    previous_states.append((prev_mouse_pos, cat_pos, prev_turn))
            return previous_states

        states_queue = deque()
        
        for i in range(1, nodes_count):
            result[HOLE][i][MOUSE_TURN] = result[HOLE][i][CAT_TURN] = MOUSE_WIN
            states_queue.append((HOLE, i, MOUSE_TURN))
            states_queue.append((HOLE, i, CAT_TURN))

            result[i][i][MOUSE_TURN] = result[i][i][CAT_TURN] = CAT_WIN
            states_queue.append((i, i, MOUSE_TURN))
            states_queue.append((i, i, CAT_TURN))

        while states_queue:
            mouse_pos, cat_pos, turn = states_queue.popleft()
            curr_result = result[mouse_pos][cat_pos][turn]

            for prev_mouse_pos, prev_cat_pos, prev_turn in get_prev_states(mouse_pos, cat_pos, turn):
                if result[prev_mouse_pos][prev_cat_pos][prev_turn] == DRAW:
                    can_win = (curr_result == MOUSE_WIN and prev_turn == MOUSE_TURN) or (curr_result == CAT_WIN and prev_turn == CAT_TURN)
                    if can_win:
                        result[prev_mouse_pos][prev_cat_pos][prev_turn] = curr_result
                        states_queue.append((prev_mouse_pos, prev_cat_pos, prev_turn))
                    else:
                        degrees[prev_mouse_pos][prev_cat_pos][prev_turn] -= 1
                        if degrees[prev_mouse_pos][prev_cat_pos][prev_turn] == 0:
                            result[prev_mouse_pos][prev_cat_pos][prev_turn] = curr_result
                            states_queue.append((prev_mouse_pos, prev_cat_pos, prev_turn))

        return result

if __name__ == "__main__":
    root = tk.Tk()
    game = CatMouseGame(root)
    root.mainloop()

