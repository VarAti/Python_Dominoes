# Write your code here
import random
import string

domino_set = []
player_set = []
computer_set = []
computer_move = ""
starting_player = ""
domino_snake = []


def init_game():
    global domino_set, player_set, computer_set, starting_player, domino_snake
    domino_set = []
    for i in range(0, 7):
        for k in range(i, 7):
            domino_set.append([i, k])
    random.shuffle(domino_set)
    player_set = [domino_set.pop() for _ in range(7)]
    computer_set = [domino_set.pop() for _ in range(7)]
    starting_domino = None
    for i in range(7):
        player_domino = player_set[i]
        computer_domino = computer_set[i]
        if player_domino[0] == player_domino[1]:
            if starting_domino is None or player_domino[0] > starting_domino[0]:
                starting_domino = player_domino
                starting_player = "computer"
        if computer_domino[0] == computer_domino[1]:
            if starting_domino is None or computer_domino[0] > starting_domino[0]:
                starting_domino = computer_domino
                starting_player = "player"
    domino_snake = [starting_domino]
    if starting_player == "player":
        computer_set.remove(starting_domino)
    else:
        player_set.remove(starting_domino)


def print_interface():
    header = '=' * 70
    print(header)
    print(f"Stock size: {len(domino_set)}")
    print(f"Computer pieces: {len(computer_set)}\n")
    print_snake()
    print(f"\nYour pieces:")
    for i in range(len(player_set)):
        print(f"{i + 1}:{player_set[i]}")
    if starting_player == 'player':
        print("\nStatus: It's your turn to make a move. Enter your command.")
    else:
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")


def print_snake():
    if len(domino_snake) < 7:
        print(" ".join(str(d) for d in domino_snake))
    else:
        print(
            f"{domino_snake[0]}{domino_snake[1]}{domino_snake[2]} ... {domino_snake[-3]}{domino_snake[-2]}{domino_snake[-1]}")


def insert_domino(which_side, player):
    side = 0 if which_side == "left" else -1
    if player == "player":
        current_player_set = player_set
        current_player_move = player_move
    else:
        current_player_set = computer_set
        current_player_move = computer_move

    first_domino = domino_snake[side]
    snake_face = first_domino[side]
    domino = current_player_set[int(current_player_move[-1]) - 1]
    if domino[side + 1] != snake_face:
        if domino[side] != snake_face:
            return False
        else:
            switched_domino = [domino[1], domino[0]]
            if side == -1:
                domino_snake.append(switched_domino)
            else:
                domino_snake.insert(0, switched_domino)
            current_player_set.remove(domino)
    else:
        if side == -1:
            domino_snake.append(domino)
        else:
            domino_snake.insert(0, domino)
        current_player_set.remove(domino)
    return True


def check_game_conditions():
    if len(player_set) == 0:
        print("Status: The game is over. You won!")
        return False
    elif len(computer_set) == 0:
        print("Status: The game is over. The computer won!")
        return False
    elif domino_snake[0][0] == domino_snake[-1][-1] \
            and " ".join(str(d) for d in domino_snake).count(str(domino_snake[0][0])) == 8:
        print("Status: The game is over. It's a draw!")
        return False
    else:
        return True


def computer_move_with_stat():
    global computer_move, starting_player, computer_set
    input()
    computer_set = sort_computer_set_with_stat()
    set_size = len(computer_set) + 1
    for i in range(1, set_size):
        computer_move = str(i)
        if insert_domino("right", "computer"):
            break
        computer_move = '-' + str(i)
        if insert_domino("left", "computer"):
            break
    else:
        if len(domino_set) > 0:
            computer_set.append(domino_set.pop())
    starting_player = "player"


def sort_computer_set_with_stat():
    sorted_computer_set = []
    domino_dict = {i: 0 for i in range(7)}
    working_set = domino_snake[:]
    working_set.extend(computer_set)
    for domino in working_set:
        domino_dict.update({domino[0]: domino_dict.get(domino[0]) + 1})
        domino_dict.update({domino[1]: domino_dict.get(domino[1]) + 1})
    while len(computer_set) > 0:
        points = 0
        index_of_domino = None
        for domino in computer_set:
            temp_points = domino_dict.get(domino[0]) + domino_dict.get(domino[1])
            if temp_points > points:
                points = temp_points
                index_of_domino = computer_set.index(domino)
        sorted_computer_set.append(computer_set.pop(index_of_domino))
    return sorted_computer_set


init_game()
print_interface()

while check_game_conditions() is True:
    if starting_player == 'player':
        player_move = input()
        if len(player_move) > 2 \
                or len(player_move) == 0 \
                or len(player_move) == 1 and player_move[0] not in string.digits \
                or len(player_move) == 2 and player_move[0] != '-' and player_move[1] not in string.digits:
            print("Invalid input. Please try again.")
            continue
        else:
            if player_move[0] == '0':
                if len(domino_set) > 0:
                    player_set.append(domino_set.pop())
            elif player_move[0] == '-':
                if not insert_domino("left", "player"):
                    print("Illegal move. Please try again.")
                    continue
            else:
                if not insert_domino("right", "player"):
                    print("Illegal move. Please try again.")
                    continue
        starting_player = "computer"
    else:
        computer_move_with_stat()
    print_interface()
