import tkinter as tk
from tkinter import messagebox

class Reverse(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=125, height=125)
        self.root = root
        self.root.geometry("1000x1000")
        self.grid()
        self.create_widgets()
        self.initialize_board()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=800, height=800, bg='green')
        self.canvas.grid(row=0, column=0, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.handle_click)

        self.turn_label = tk.Label(self, text="黒側の番", font=("Helvetica", 16))
        self.turn_label.grid(row=1, column=0, pady=10)

    def initialize_board(self):
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.current_turn = 'black'

        self.board[3][3] = 'white'
        self.board[3][4] = 'black'
        self.board[4][3] = 'black'
        self.board[4][4] = 'white'

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                x0 = i * 100
                y0 = j * 100
                x1 = x0 + 100
                y1 = y0 + 100
                self.canvas.create_rectangle(x0, y0, x1, y1, fill='green')
                if self.board[i][j] == 'black':
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill='black')
                elif self.board[i][j] == 'white':
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill='white')

    def handle_click(self, event):
        x = event.x // 100
        y = event.y // 100
        if self.is_valid_move(x, y, self.current_turn):
            self.board[x][y] = self.current_turn
            self.flip_discs(x, y, self.current_turn)
            self.current_turn = 'white' if self.current_turn == 'black' else 'black'
            self.turn_label.config(text=f"{self.current_turn.capitalize()}'の番")
            self.draw_board()
            if not self.has_valid_moves(self.current_turn):
                self.current_turn = 'white' if self.current_turn == 'black' else 'black'
                if not self.has_valid_moves(self.current_turn):
                    self.end_game()

    def is_valid_move(self, x, y, color):
        if self.board[x][y] != '':
            return False
        opponent_color = 'white' if color == 'black' else 'black'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] == opponent_color:
                while 0 <= nx < 8 and 0 <= ny < 8:
                    nx += dx
                    ny += dy
                    if not (0 <= nx < 8 and 0 <= ny < 8):
                        break
                    if self.board[nx][ny] == '':
                        break
                    if self.board[nx][ny] == color:
                        return True
        return False

    def flip_discs(self, x, y, color):
        opponent_color = 'white' if color == 'black' else 'black'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            discs_to_flip = []
            while 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] == opponent_color:
                discs_to_flip.append((nx, ny))
                nx += dx
                ny += dy
            if 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] == color:
                for flip_x, flip_y in discs_to_flip:
                    self.board[flip_x][flip_y] = color

    def has_valid_moves(self, color):
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j, color):
                    return True
        return False

    def end_game(self):
        black_count = sum(row.count('black') for row in self.board)
        white_count = sum(row.count('white') for row in self.board)
        winner = "黒の勝ち" if black_count > white_count else "白の勝ち" if white_count > black_count else "No one"
        messagebox.showinfo("ゲーム終了", f"黒の数: {black_count}\n白の数: {white_count}\n勝者: {winner}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Reverse(root)
    root.mainloop()
