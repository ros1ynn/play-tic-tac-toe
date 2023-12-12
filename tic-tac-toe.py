import tkinter as tk
from tkinter import simpledialog, messagebox

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Play Tic-Tac-Toe!")

        # prompt users to add player names
        self.player1 = simpledialog.askstring("Player 1", "Enter Player 1's name:")
        self.player2 = simpledialog.askstring("Player 2", "Enter Player 2's name:")

        self.current_player = self.player1
        self.player1_wins = 0
        self.player2_wins = 0
        self.draws = 0
        self.upgrade_threshold = 3
        self.grid_size = 3
        # flag to track whether the grid has been upgraded
        self.grid_upgraded = False  

        # add labels to display player names, score, and draw counter on screen
        self.label_player1 = tk.Label(self.master, text=f"{self.player1}'s Wins:")
        self.label_player1.grid(row=0, column=self.grid_size)

        self.label_player2 = tk.Label(self.master, text=f"{self.player2}'s Wins:")
        self.label_player2.grid(row=1, column=self.grid_size)

        self.label_draws = tk.Label(self.master, text="Draws:")
        self.label_draws.grid(row=2, column=self.grid_size)

        self.player1_score_label = tk.Label(self.master, text="0")
        self.player1_score_label.grid(row=0, column=self.grid_size + 1)

        self.player2_score_label = tk.Label(self.master, text="0")
        self.player2_score_label.grid(row=1, column=self.grid_size + 1)

        self.draws_label = tk.Label(self.master, text="0")
        self.draws_label.grid(row=2, column=self.grid_size + 1)

        # create buttons for the Tic-Tac-Toe grid
        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j] = tk.Button(self.master, text="", font=('normal', 20), width=6, height=2,
                                              command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

        self.reset_board()

    def on_click(self, row, col):
        if self.buttons[row][col]["text"] == "":
            self.buttons[row][col]["text"] = "X" if self.current_player == self.player1 else "O"
            if self.check_winner(row, col):
                # prompt message for winner
                messagebox.showinfo("Winner!", f"{self.current_player} wins!")
                if self.current_player == self.player1:
                    self.player1_wins += 1
                    self.player1_score_label.config(text=str(self.player1_wins))
                else:
                    self.player2_wins += 1
                    self.player2_score_label.config(text=str(self.player2_wins))

                if not self.grid_upgraded and (self.player1_wins + self.player2_wins) % self.upgrade_threshold == 0 and (self.player1_wins + self.player2_wins) > 0:
                    self.upgrade_grid()
                    # upgrade the game difficulties after three wins of either player
                    self.grid_upgraded = True  

                self.reset_board()


            # prompts a message when there is a draw
            elif self.check_draw():
                messagebox.showinfo("Draw", "It's a draw!")
                self.draws += 1
                self.draws_label.config(text=str(self.draws))
                self.reset_board()

            else:
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    # check for winner 
    def check_winner(self, row, col):
        # check row
        if self.check_line(self.buttons[row]):
            return True
        # check column
        if self.check_line([self.buttons[i][col] for i in range(self.grid_size)]):
            return True
        # check diagonals
        if row == col and self.check_line([self.buttons[i][i] for i in range(self.grid_size)]):
            return True
        if row + col == self.grid_size - 1 and self.check_line([self.buttons[i][self.grid_size - 1 - i] for i in range(self.grid_size)]):
            return True
        return False

    def check_line(self, line):
        return all(button["text"] == line[0]["text"] and button["text"] != "" for button in line)

    def check_draw(self):
        return all(self.buttons[i][j]["text"] != "" for i in range(self.grid_size) for j in range(self.grid_size))

    def reset_board(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j]["text"] = ""

        self.current_player = self.player1

    # upgrade grid size to 5*5
    def upgrade_grid(self):
        self.grid_size = min(self.grid_size * 2, 5)  
        messagebox.showinfo("Grid Upgrade", f"Grid size upgraded to {self.grid_size}x{self.grid_size}!")

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if i >= len(self.buttons):
                    self.buttons.append([])
                if j >= len(self.buttons[i]):
                    button = tk.Button(self.master, text="", font=('normal', 20), width=6, height=2,
                                       command=lambda row=i, col=j: self.on_click(row, col))
                    button.grid(row=i, column=j)
                    self.buttons[i].append(button)
                else:
                    self.buttons[i][j]["text"] = ""

        # reset labels to maintain players' names and the counter's visibility after the grid upgrade
        self.label_player1.grid(row=0, column=self.grid_size)
        self.label_player2.grid(row=1, column=self.grid_size)
        self.label_draws.grid(row=2, column=self.grid_size)
        self.player1_score_label.grid(row=0, column=self.grid_size + 1)
        self.player2_score_label.grid(row=1, column=self.grid_size + 1)
        self.draws_label.grid(row=2, column=self.grid_size + 1)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
