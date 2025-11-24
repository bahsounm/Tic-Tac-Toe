import random as rand
from user_manager import User
import os

class GameManager:
    def __init__(self, board):
        self.board = board
        self.players = None
        self.cpu_difficulty = None

    def show_rules_board(self):
        rules = [
            ["1","2","3"],
            ["4","5","6"],
            ["7","8","9"]
        ]

        print("RULES / POSITIONS:")
        print(self.render_board(rules))
        print("\nPick a number 1-9 to place your token there.")
        input("\nPress ENTER to start the game...")
    
    def render_board(self, board=None):
        if board is None:
            board = self.board

        display = ""
        i = 0

        for row in board:
            row_string = ""
            i += 1
            for col in row:
                row_string += f" {col} |"
            display += row_string[:-1]
            if i < 3:
                display += "\n-----------\n"

        return display

    def play_game(self):
        self.create_players()

        # Randomize who goes first
        p1 = rand.choice(self.players)
        p2 = self.players[1] if p1 == self.players[0] else self.players[0]

        os.system("cls")
        print("Player going first:", p1.name)
        print("Second player:", p2.name)
        print()

        self.show_rules_board()
        os.system("cls")

        # Detect CPU correctly
        cpu_player = None
        for player in self.players:
            if player.name.lower() == "cpu":
                cpu_player = player
                break

        current_player = p1

        while True:
            print(self.render_board())

            # CPU turn
            if current_player == cpu_player:
                if self.cpu_difficulty == "easy":
                    choice = self.cpu_move_easy()
                else:
                    # find human player's token to block properly
                    human = p1 if cpu_player == p2 else p2
                    choice = self.cpu_move_medium(cpu_player.token, human.token)

                print(f"\nCPU chooses {choice}")

            else:
                # Human turn
                choice = input(f"{current_player.name} choose (1-9): ").strip()

            # Try placing
            if not self.place_piece(choice, current_player.token):
                continue

            winner = self.check_win_condition()
            if winner:
                print(self.render_board())
                print(f"\nWinner is {current_player.name}!")
                break

            if all(c != " " for row in self.board for c in row):
                print(self.render_board())
                print("\nIt's a tie!")
                break

            # Switch turns
            current_player = p2 if current_player == p1 else p1
            os.system("cls")

    def create_players(self):
        p1_token, p2_token = self.select_tokens()
        p1_name, p2_name = self.select_names()

        # If player 2 is CPU, ask for difficulty
        if p2_name.lower() == "cpu":
            self.cpu_difficulty = self.select_cpu_difficulty()

        self.players = [
            User(p1_name, p1_token),
            User(p2_name, p2_token)
        ]

    def select_names(self):
        p1 = input("Player 1 name (default: Player 1): ").strip()
        p2 = input("Player 2 name (default: Player 2): ").strip()

        if p1 == "":
            p1 = "Player 1"
        if p2 == "":
            p2 = "Player 2"

        return p1, p2
    
    def select_tokens(self):
        while True:
            p1_choice = input("Player 1: Choose X or O: ").upper()

            if p1_choice == "X":
                return "X", "O"

            if p1_choice == "O":
                return "O", "X"

            print("Invalid choice. Please choose X or O.")

    def check_win_condition(self):
        board = self.board
        # check the rows
        for row in board:
            if (row[0] != " ") and (row[0] == row[1] and row[1] == row[2]):
                return row[0]
        # check the columns
        for col in range(0,3):
            if (board[0][col] != " ") and (board[0][col] == board[1][col] and board[1][col] == board[2][col]):
                return board[0][col]
        # check diagonals
        if (board[0][0] != " ") and (board[0][0] == board[1][1] == board[2][2]):
            return board[0][0]

        if (board[0][2] != " ") and (board[0][2] == board[1][1] == board[2][0]):
            return board[0][2]
        return None

    def place_piece(self, choice, token):
        pos_map = {
            "1": (0,0), "2": (0,1), "3": (0,2),
            "4": (1,0), "5": (1,1), "6": (1,2),
            "7": (2,0), "8": (2,1), "9": (2,2),
        }

        if choice not in pos_map:
            print("Invalid position. Choose 1-9.")
            return False

        r, c = pos_map[choice]

        if self.board[r][c] != " ":
            print("That spot is taken. Try again.")
            return False

        self.board[r][c] = token
        return True

    # This is if we want to face the cpu and not a second player
    def get_empty_positions(self):
        empties = []
        pos_map = {
            "1": (0,0), "2": (0,1), "3": (0,2),
            "4": (1,0), "5": (1,1), "6": (1,2),
            "7": (2,0), "8": (2,1), "9": (2,2),
        }

        for pos, (r,c) in pos_map.items():
            if self.board[r][c] == " ":
                empties.append(pos)

        return empties

    def cpu_move_easy(self):
        empties = self.get_empty_positions()
        return rand.choice(empties)

    def cpu_move_medium(self, cpu_token, human_token):
        pos_map = {
        "1": (0,0), "2": (0,1), "3": (0,2),
        "4": (1,0), "5": (1,1), "6": (1,2),
        "7": (2,0), "8": (2,1), "9": (2,2),
        }
        empties = self.get_empty_positions()

        for pos in empties:
            r,c = pos_map[pos]
            self.board[r][c] = cpu_token
            if self.check_win_condition() == cpu_token:
                r,c = pos_map[pos]
                self.board[r][c] = " "
                return pos
            r,c = pos_map[pos]
            self.board[r][c] = " "

        for pos in empties:
            r,c = pos_map[pos]
            self.board[r][c] = human_token
            if self.check_win_condition() == human_token:
                r,c = pos_map[pos]
                self.board[r][c] = " "
                return pos
            r,c = pos_map[pos]
            self.board[r][c] = " "

        return rand.choice(empties)

    def select_cpu_difficulty(self):
        while True:
            print("\nCPU Difficulty:")
            print("1) Easy")
            print("2) Medium")
            choice = input("Choose difficulty (1 or 2): ").strip()

            if choice == "1":
                return "easy"
            elif choice == "2":
                return "medium"
            else:
                print("Invalid option. Please select 1 or 2.")
