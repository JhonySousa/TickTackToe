from easyansi import cursor, screen
import getkey

# Posição do cursor no terminal...
WIN_POS = cursor.get_location()


def clear(n_lines: int):
    """
    Clear some number of lines.
    """
    for r in range(n_lines+1):
        screen.clear_line(WIN_POS[1] + r)


def draw_game(game_status) -> tuple:
    """
    Mostra o tabuleiro do jogo.
    """
    print('\033[7m   0   1   2\n \033[m')
    cords = 0
    for line in game_status:
        print(f'\033[7m{cords}\033[m  {line[0]} | {line[1]} | {line[2]}')
        if cords < 2:
            print('\033[7m \033[m ' + '-'*11)
        cords += 1


def draw_menu(menu_opts) -> int:
    """
    Função que desenha na tela um menu

    :param menu_opts: Lista ou tupla contendo as opções
    :return: o index da opção selecionada
    """
    selected = 0
    cursor.hide()
    while True:
        cursor.locate(WIN_POS[0], WIN_POS[1])
        for opt in menu_opts:
            if selected == menu_opts.index(opt):
                print('\033[7m', end='')
            print(opt + '\033[m')
        key = getkey.getkey()

        clear(len(menu_opts))

        if key == getkey.keys.UP and selected > 0:
            selected -= 1
        elif key == getkey.keys.DOWN and selected < len(menu_opts)-1:
            selected += 1
        elif key == getkey.keys.ENTER:
            break
    cursor.show()
    return selected


def check_game(game_status: list) -> int:
    """-> Verifica se o jogo já a cabou.

    :param game_status: É o estado do game.
    :return: as opções de retorno são
        1: Retorna o indice do jogador que ganhou.
        2: Retorna -1 se o jogo ainda não acabou.
        3: Retorna 3 se deu velha.
    """

    # Horizontal lines
    for line in game_status:
        if line[0] == line[1] == line[2] != ' ':
            return 0 if line[0] == 'O' else 1

    # Vertical Lines
    for row in range(3):
        if game_status[0][row] == game_status[1][row] == game_status[2][row] != ' ':
            return 0 if game_status[0][row] == 'O' else 1

    # Inclinada
    if game_status[0][0] == game_status[1][1] == game_status[2][2] != ' ':
        return 0 if game_status[0][0] == 'O' else 1
    elif game_status[0][2] == game_status[1][1] == game_status[2][0] != ' ':
        return 0 if game_status[0][2] == 'O' else 1

    # Verifica velha
    for line in game_status:
        for element in line:
            if element == ' ':
                return -1
    return 3


main_menu = ('New', 'Quit')
opt = draw_menu(main_menu)

# Exit Game
if opt == 1:
    exit()

game_end = -1
default_pos = (WIN_POS[0]+3, WIN_POS[1]+2)
selection = [0, 0]
player = True
cursor.show()

game_status = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]
last_pos = default_pos
while game_end < 0:
    cursor.locate(WIN_POS[0], WIN_POS[1])
    draw_game(game_status)
    print(f'\n\033[32mEstá na vez do jogador {int(player)+1}\033[m')
    cursor.locate(last_pos[0], last_pos[1])

    while True:
        key = getkey.getkey()
        if key == getkey.keys.UP and selection[1] > 0:
            selection[1] -= 1
        elif key == getkey.keys.DOWN and selection[1] < 2:
            selection[1] += 1
        elif key == getkey.keys.LEFT and selection[0] > 0:
            selection[0] -= 1
        elif key == getkey.keys.RIGHT and selection[0] < 2:
            selection[0] += 1
        elif (
            key == getkey.keys.ENTER and
            game_status[selection[1]][selection[0]] == ' '
        ):
            game_status[selection[1]][selection[0]] = 'O' if player else 'X'
            break

        cursor.locate(
            default_pos[0] + selection[0] * 4,
            default_pos[1] + selection[1] * 2
        )
    game_end = check_game(game_status)
    player = not player
    last_pos = cursor.get_location()

cursor.locate(WIN_POS[0], WIN_POS[1])
draw_game(game_status)
screen.clear_line(WIN_POS[1]+9)
if game_end == 3:
    print('\033[1mDeu velha...\033[m')
else:
    print(f'\033[1;5;32mO Player {game_end+1} GANHOU!!\033[m')
