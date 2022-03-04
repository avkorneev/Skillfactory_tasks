from InnerLogic import Dot, Ship, Board, PlaceShipError
from random import randint


class Player:
    def __init__(self, enemy_board):
        self.enemy_board = enemy_board

    def move(self, board):
        move_coords = self.ask()
        print(move_coords)
        return board.board_shot(move_coords)


class User(Player):
    def ask(self):
        coord = input("Input coordinates in format row and column separated by a space:").split()
        while True:
            try:
                return Dot(int(coord[0]) - 1, int(coord[1]) - 1)
            except IndexError:
                coord = input("Input coordinates separated by a space!").split()
            except AttributeError:
                coord = input("Input coordinates separated by a space!").split()
            except ValueError:
                coord = input("Input coordinates separated by a space!").split()

class AI(Player):
    def ask(self):
        return Dot(randint(0, len(self.enemy_board.board) - 1), randint(0, len(self.enemy_board.board) - 1))


class Game:
    def greet(self):
        print("----------Welcome to Battleships!----------")
        print("Coordinates input format: row column (example: 5 6)")
        size = 0
        while size < 10:  # number of ships suits for 10x10 board or bigger
            try:
                size = int(input("Input board size (10 or bigger):"))
            except ValueError:
                print("Input a number!")
        return size

    def loop(self, size):
        turn = 0
        self.user_board = None
        self.ai_board = None
        while self.user_board is None: # generating boards.
            self.user_board = self.random_board(size)
        while self.ai_board is None:
            self.ai_board = self.random_board(size)
        self.ai_board.hid = 1
        while True:
            turn += 1
            print("Move number", turn, "!")
            print("----------User board----------")
            print(self.user_board)
            print("\n")
            print("----------AI board----------")
            print(self.ai_board)
            print("\n")
            if turn % 2 == 1:
                print("User's turn:")
                while User(self.ai_board).move(self.ai_board):
                    print("Move number", turn, "!")
                    print("----------User board----------")
                    print(self.user_board)
                    print("\n")
                    print("----------AI board----------")
                    print(self.ai_board)
                    print("\n")
            if turn % 2 == 0:
                print("AI's turn:")
                while AI(self.user_board).move(self.user_board):
                    print("Move number", turn, "!")
                    print("----------User board----------")
                    print(self.user_board)
                    print("\n")
                    print("----------AI board----------")
                    print(self.ai_board)
                    print("\n")
            if self.ai_board.ships_alive == 0:
                print("¯\_(ツ)_/¯ " * 10)
                print("User won!")
                print("Congratulations!")
                print("Thanks for playing!")
                break
            if self.user_board.ships_alive == 0:
                print("¯\_(ツ)_/¯ " * 20)
                self.ai_board.hid = 0
                print("----------User board----------")
                print(self.user_board)
                print("\n")
                print("----------AI board----------")
                print(self.ai_board)
                print("AI won!")
                print("Better luck next time!")
                print("Thanks for playing!")
                break

    def random_board(self, board_size):
        ship_sizes = [4,3,3,2,2,2,1,1,1,1]     #this list contains sizes of ships (and their number)

        board_empty = [[]]
        for i in range(board_size):
            for j in range(board_size):
                board_empty[i].append(" ")
            board_empty.append([])
        board_empty.pop()

        board = Board(board_empty, ships=[], hid=0, ships_alive=0)  # defaults for board
        attempts = 0
        for i in ship_sizes:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                a = Ship(i, Dot(randint(0, board_size - 1), randint(0, board_size - 1)), randint(0, 1), i)
                try:
                    board.add_ship(a)
                    break
                except PlaceShipError:
                    pass
        for i in range(board_size):  # After generating the board we can remove (·) contouring ships
            for j in range(board_size):
                board.board[i][j] = board.board[i][j].replace('·', ' ')

        return board

    def start(self):
        size = self.greet()
        self.loop(size)
