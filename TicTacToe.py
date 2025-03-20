import tkinter as tk
import random

class TicTacToe:
    def __init__(self):
       # Initialize empty board (using ' ' for empty squares)
       self.board = [" " for _ in range(9)]
       self.human_player = "O"
       self.ai_player = "X"

    # def print_board(self):
    #    """Print the current state of the board"""
    #    for i in range(0, 9, 3):
    #        print(f"{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}")
    #        if i < 6:
    #            print("---------")

    def available_moves(self):
       """Returns list of available moves (indices of empty squares)"""
       return [i for i, spot in enumerate(self.board) if spot == " "]
   
    def make_move(self, position, player):
       """Make a move on the board"""
       if self.board[position] == " ":
           self.board[position] = player
           return True
       return False
   
    def is_board_full(self):
       """Check if the board is full"""
       return " " not in self.board
   
    def check_winner(self):
         """Check if there is a winner"""
         winning_combinations = [
              (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
              (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
              (0, 4, 8), (2, 4, 6)  # Diagonals
         ]
         for combo in winning_combinations:
              if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
                return self.board[combo[0]]
         return None
    
    def game_over(self):
       """Check if the game is over"""
       return self.check_winner() is not None or self.is_board_full()
    
    # ----------------- Minimax algorithm implementation -----------------
    
    """
    depth - Tracks how many levels deep we are in the recursion. 
    This can be used to limit search depth for very complex games, 
    though for tic-tac-toe we don't need to limit it.
    """

    """
    is_maximizing - A boolean flag indicating whether we're currently looking for
    the maximum score (AI's turn) or minimum score (human's turn). 
    This alternates with each recursive call as players take turns.
    """
    def minimax(self, depth, is_maximizing):
        """
        Minimax algorithm implementation
        Returns the best score possible for the current board state
        """
        # Base cases
        winner = self.check_winner()
        if winner == self.ai_player:
           return 1
        if winner == self.human_player:
           return -1
        if self.is_board_full():
           return 0
       
        # if it is the maximizing player's turn (AI), we want to maximize the score
        if is_maximizing:
            best_score = float("-inf")
            for move in self.available_moves():
                # Make a calculating move
                self.board[move] = self.ai_player
                # Recursively call minimax with the next depth and the minimizing player
                score = self.minimax(depth + 1, False)
                # Reset the move
                self.board[move] = " "
                # Update the best score
                best_score = max(score, best_score)
            return best_score
        
        # if it is the minimizing player's turn (human), we want to minimize the score
        else:
        # if it is the minimizing player's turn (human), we want to minimize the score
            best_score = float("inf")
            for move in self.available_moves():
                # Make a calculating move
                self.board[move] = self.human_player
                # Recursively call minimax with the next depth and the maximizing player
                score = self.minimax(depth + 1, True)
                # Reset the move
                self.board[move] = " "
                # Update the best score
                best_score = min(score, best_score)
            return best_score


    def get_best_move(self):
       """Find the best move for AI using minimax"""
       best_score = float("-inf")
       best_move = None

       for move in self.available_moves():
           # Make a calculating move
           self.board[move] = self.ai_player
           # Recursively call minimax with the next depth and the minimizing player
           score = self.minimax(0, False)
           # Reset the move
           self.board[move] = " "

           # Update the best score
           if score > best_score:
               best_score = score
               best_move = move

       return best_move
    
    # def play_game(self):
    #     """Main game loop"""
    #     print("Welcome to Tic Tac Toe!")
    #     print("You are 'O' and the AI is 'X'")
    #     print("Enter positions (0-8) as shown below:")
    #     print("0 | 1 | 2")
    #     print("---------")
    #     print("3 | 4 | 5")
    #     print("---------")
    #     print("6 | 7 | 8")
    #     print("\n")


    #     # Randomly decide who goes first

    #     ai_turn = random.choice([True, False])

    #     while not self.game_over():
    #         self.print_board()

    #         if ai_turn:
    #             print("\nAI's turn...")
    #             move = self.get_best_move()
    #             self.make_move(move, self.ai_player)
    #         else:
    #             while True:
    #                 try:
    #                     move = int(input("\nYour turn (0-8): "))
    #                     if 0 <= move <= 8 and self.make_move(move, self.human_player):
    #                         break
    #                     else:
    #                         print("Invalid move! Try again.")
    #                 except ValueError:
    #                     print("Please enter a number between 0 and 8!")

    #         ai_turn = not ai_turn
        
    #     # Game over
    #     self.print_board()
    #     winner = self.check_winner()
    #     if winner == self.ai_player:
    #         print("\nAI wins!")
    #     elif winner == self.human_player:
    #         print("\nCongratulations! You win!")
    #     else:
    #         print("\nIt's a tie!")

class TicTacToeGUI: 
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.game = TicTacToe()
        self.buttons = []

        self.ai_turn = random.choice([True, False])
        self.create_widgets()
        if self.ai_turn:
            self.master.after(500, self.ai_move)

    def create_widgets(self):
        for i in range(9):
            btn = tk.Button(self.master, text=" ", font=("Helvetica", 32), width=4, height=2, command=lambda i=i: self.human_move(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

    def human_move(self, index):
        """Human's turn"""
        if self.game.board[index] == " " and not self.game.game_over() and not self.ai_turn:
            self.game.make_move(index, self.game.human_player)
            self.buttons[index]["text"] = self.game.human_player
            if self.game.game_over():
                self.end_game()
            else:
                self.ai_turn = True
                self.master.after(500, self.ai_move)


    def ai_move(self):
        """IA's turn"""
        if not self.game.game_over():
            move = self.game.get_best_move()
            if move is not None:
                self.game.make_move(move, self.game.ai_player)
                self.buttons[move]["text"] = self.game.ai_player
        self.ai_turn = False
        if self.game.game_over():
            self.end_game()


    def end_game(self):
        """Display the result of the game and disable the buttons"""
        winner = self.game.check_winner()
        if winner:
            result = f"{winner} wins !"
        else:
            result = "It's a tie!"
        for btn in self.buttons:
            btn.config(state="disabled")
        result_label = tk.Label(self.master, text=result, font=("Helvetica", 24))
        result_label.grid(row=3, column=0, columnspan=3)

    
            
# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()