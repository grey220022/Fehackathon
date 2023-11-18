import tkinter as tk
import tkinter.messagebox
import subprocess
import configparser

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = [""] * 9
        self.current_player = "X"
        self.buttons = []
        self.create_board()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.contractaddress = config.get('settings', 'contract_address')
        self.privatekey = config.get('settings', 'private_key')
        command = ['cast', 'send', '--rpc-url', 'http://localhost:8545', '--private-key', self.privatekey, self.contractaddress, 'init()']
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


    def create_board(self):
        for i in range(9):
            button = tk.Button(self.root, text="", font=('normal', 40), width=5, height=2,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def on_button_click(self, i):
        if self.board[i] == "":
            self.board[i] = self.current_player
            self.buttons[i].config(text=self.current_player)
            if self.check_winner(i):
                tkinter.messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif "" not in self.board:
                tkinter.messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, i):
        command = ['cast', 'send', '--rpc-url', 'http://localhost:8545', '--private-key', self.privatekey, self.contractaddress,'make_move(uint8)', str(i)]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        command = ['cast', 'call', '--rpc-url', 'http://localhost:8545', self.contractaddress, 'get_gamestatus()']
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "0x0000000000000000000000000000000000000000000000000000000000000000" in result.stdout: # return 0 from the smart contract
            print("Game is not over")
            return False
        else:
            print("Game is over")
            return True
    def reset_game(self):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="")
        self.current_player = "X"
        command = ['cast', 'send', '--rpc-url', 'http://localhost:8545', '--private-key', self.privatekey, self.contractaddress, 'init()']
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
