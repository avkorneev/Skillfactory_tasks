class Dot:
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord

    def __eq__(self, other):
        return self.x_coord == other.x_coord and self.y_coord == other.y_coord

    def __repr__(self):
        return f"Dot{self.x_coord + 1, self.y_coord + 1}"


class Ship:
    def __init__(self, ship_size, ship_coord, ship_dir, ship_hp):
        self.ship_size = ship_size
        self.ship_coord = ship_coord
        self.ship_dir = ship_dir
        self.ship_hp = ship_hp

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.ship_size):
            x_ship = self.ship_coord.x_coord
            y_ship = self.ship_coord.y_coord
            if self.ship_dir == 0:  # ship will be horizontal
                x_ship += i
            elif self.ship_dir == 1:  # ship will be vertical
                y_ship += i
            ship_dots.append(Dot(x_ship, y_ship))
        return ship_dots

    def shot(self, other):
        return other in self.dots


class PlaceShipError(Exception):
    pass


class Board:
    def __init__(self, board, ships, hid, ships_alive):
        self.board = board
        self.ships = ships
        self.hid = hid
        self.ships_alive = ships_alive

    def __str__(self):
        res = "  "
        for i in range(len(self.board[0])):
            if i < 10:  # This one is needed so that board would not shift at size > 10 due to two-digit numbers
                res += " "
            res += f"| {i + 1}"
        for i in range(len(self.board)):
            res += ' |'
            res += '\n'
            res += f"{i + 1}"
            if i + 1 < 10:  # This one is needed so that board would not shift at size > 10 due to two-digit numbers
                res += " "
            for j in range(len(self.board[i])):
                res += " | "
                res += self.board[i][j]
        res += ' |'
        if self.hid == 1:
            res = res.replace('█', ' ')
        return res

    def add_ship(self, new_ship):  # method adding new ships
        busy_check = 0
        for i in range(new_ship.ship_size):  # This cycle checks if any point of new ship is already busy
            if self.out(new_ship.dots[i]):
                raise PlaceShipError()
            if self.board[new_ship.dots[i].x_coord][new_ship.dots[i].y_coord] != ' ':
                busy_check = 1
        if busy_check == 0:  # If not - we can't place the ship
            for i in range(new_ship.ship_size):
                self.board[new_ship.dots[i].x_coord][new_ship.dots[i].y_coord] = '█'
            self.ships.append(new_ship)
            self.contour(new_ship)
            self.ships_alive += 1
        else:
            raise PlaceShipError()

    def out(self, dot):  # method checking that dot is within game board
        return not ((0 <= dot.x_coord < len(self.board)) and (0 <= dot.y_coord < len(self.board)))

    def contour(self, ship):  # method contouring specific ship and not letting to place ships around it
        cont = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1)]  # list of points around the given point
        for i in ship.dots:  # checking all points of the ship
            for k in cont:
                if not self.out(Dot(k[0] + i.x_coord, k[1] + i.y_coord)):  # checking that surrounding point is not
                    # out of board
                    if self.board[k[0] + i.x_coord][k[1] + i.y_coord] != '█' and self.board[k[0] + i.x_coord][
                        k[1] + i.y_coord] != 'X':
                        self.board[k[0] + i.x_coord][k[1] + i.y_coord] = '·'
        return self.board

    def board_shot(self, dot):  # returns True if one more turn is required (successful shot, busy point,
        # out of board point), otherwise returns False
        if not self.out(dot):
            if self.board[dot.x_coord][dot.y_coord] == '·' or self.board[dot.x_coord][
                dot.y_coord] == 'X' or self.board[dot.x_coord][dot.y_coord] == '0':
                print("There is nothing to do in this point... Choose another one!")
                return True
            elif self.board[dot.x_coord][dot.y_coord] == '█':
                print("Nice shot!")
                self.board[dot.x_coord][dot.y_coord] = 'X'
                for i in self.ships:
                    if Dot(dot.x_coord, dot.y_coord) in i.dots:
                        i.ship_hp -= 1
                        if i.ship_hp == 0:
                            print("Ship sunk!")
                            self.ships_alive -= 1
                            self.contour(i)
                            if self.ships_alive == 0:
                                return False  # if the last ship was sunk it's time to break the cycle
                return True
            elif self.board[dot.x_coord][dot.y_coord] == ' ':
                print("You missed!")
                self.board[dot.x_coord][dot.y_coord] = '0'
                return False
        else:
            print("Point out of board, choose another one!")
            return True
