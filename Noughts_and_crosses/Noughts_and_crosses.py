##############CHANGELOG
global field
global player
global turns
# Common principle: move -> modify field -> initialise field -> check win condition -> swap players -> move...
# Field contains current game board state
field = [[]]
field[0] = [' ', '0', '1', '2']
field.append([])
field[1] = ['0', '-', '-', '-']
field.append([])
field[2] = ['1', '-', '-', '-']
field.append([])
field[3] = ['2', '-', '-', '-']
# X are starting the game
player = 'X'
turns = 1


def swap_players():  # This function swaps player when needed
    global player
    global turns
    if player == 'X':
        player = 'O'
    else:
        player = 'X'
    turns += 1

def initialise_field():  # This function draws game board
    for i in field:
        for j in i:
            print(j, end=" ")
        print('')
    print('\n')

def win_condition():  # This function checks if the current player have won. Checking filled row/column/diagonal
    for i in range(4):
        if field[1][i] == field[2][i] == field[3][i] == player or field[i][1] == field[i][2] == field[i][3] == player:
            print("Игрок", player, "побеждает!")
            return None
    if field[1][1] == field[2][2] == field[3][3] == player or field[1][3] == field[2][2] == field[3][1] == player:
        print("Игрок", player, "побеждает!")
        return None
    if turns == 9:  # Check if any fields are available
        print("Все клетки заполнены, ничья!")
        return None
    swap_players()  # If win condition hasn't been reached, next player is making his move
    move()


def modify_field(row, col):  # This function will modify field when player makes his move
    if field[row + 1][col + 1] == '-':
        field[row + 1][col + 1] = player
    else:
        print("Эта ячейка уже занята! Выберите другую")  # Unless the chosen cell has already been taken
        move()
        return None
    initialise_field()
    win_condition()


def move():  # This function will acquire coordinates of player's move
    print("Ход игрока", player, "!")
    coords = input("Введите координаты в формате строка и столбец через пробел:").split()
    modify_field(int(coords[0]), int(coords[1]))


initialise_field()
move()
