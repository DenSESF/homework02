import random
import time


def draw_game_board(f):
    len_f = len(f)
    print(' ', *list(range(len_f)))
    for i in range(len_f):
        print(i, ' '.join(f[i]))


def input_coordinates(f):
    local_x, local_y = None, None
    max_index_f = len(f) - 1
    print('Первая координата по горизонтали, вторая по вертикали')
    while True:
        cell = input('Введите координаты клетки: ').split()
        if len(cell) != 2:
            print('Введите две координаты через пробел.')
            continue
        elif any(not (c.isdigit()) for c in cell):
            print(f'Введите цифры от 0 до {max_index_f}')
            continue
        elif any(not (0 <= int(c) <= max_index_f) for c in cell):
            print('Одна или обе координаты вне диапазона.')
            continue

        local_x, local_y = map(int, cell)
        if f[local_y][local_x] != '-':
            print(f'Клетка занята - {f[local_y][local_x]}')
            continue
        break

    return local_x, local_y


def gen_bot_coord(f, h):
    def check_last_step():  # Проверка на последний ход противника
        nonlocal h, i, j, x, y, f, row
        loc_h = 'x' if h != 'x' else 'o'
        # Проверка строк
        warn_coord = []
        x, y = None, None
        for i, row in enumerate(f):
            if row.count(loc_h) == len(row) - 1 and '-' in row:
                x = row.index('-')
                y = i
                warn_coord.append((x, y))
            # Проверка колонок
            colum = list(f[j][i] for j in range(len(f)))
            if colum.count(loc_h) == len(colum) - 1 and '-' in colum:
                x = i
                y = colum.index('-')
                warn_coord.append((x, y))

        # Проверка диагонали \
        diagonal = list(f[i][i] for i in range(len(f)))
        if diagonal.count(loc_h) == len(diagonal) - 1 and '-' in diagonal:
            x = diagonal.index('-')
            y = x
            warn_coord.append((x, y))

        # Проверка диагонали /
        diagonal = list(f[len(f) - 1 - i][i] for i in range(len(f)))
        if diagonal.count(loc_h) == len(diagonal) - 1 and '-' in diagonal:
            x = diagonal.index('-')
            y = len(diagonal) - 1 - x
            warn_coord.append((x, y))

        if x is not None and y is not None:
            x, y = warn_coord[random.randrange(0, len(warn_coord))]
            return True
        else:
            return False

    free_coord = []
    # Построение списка координат и вывод случайной координаты
    for i, row in enumerate(f):
        for j, cell in enumerate(row):
            if cell == '-':
                free_coord.append((j, i))
    yield free_coord[random.randrange(0, len(free_coord))]

    x, y = None, None
    while True:
        if check_last_step():
            yield x, y

        while x is None or y is None:
            i = random.randrange(0, len(free_coord))
            x, y = free_coord[i]
            if f[y][x] == '-':
                yield x, y
            else:
                free_coord.remove((x, y))
                x, y = None, None


def decorator_time(fn):
    def wrapper(*args, **kwargs):
        print('Проверяем ход на выигрыш.')
        t0 = time.time()
        result = fn(*args, **kwargs)
        dt = time.time() - t0
        print(f"Проверка завершена. Время: {dt:.10f}")
        return result
    return wrapper


# @decorator_time
# # Проверяет все возможные выигрышные комбинации
# def check_winners(f, h):
#     # Проверка строк
#     for i in range(len(f[0])):
#         if f[i].count(h) == len(f[i]):
#             return True
#         # Проверка колонок
#         colum = list(f[j][i] for j in range(len(f)))
#         if colum.count(h) == len(f):
#             return True
#     # Проверка диагонали \
#     diagonal = list(f[i][i] for i in range(len(f)))
#     if diagonal.count(h) == len(f):
#         return True
#     # Проверка диагонали /
#     diagonal = list(f[len(f) - 1 - i][i] for i in range(len(f)))
#     if diagonal.count(h) == len(f):
#         return True
#     return False


@decorator_time
# Проверяет выигрышные комбинации по текущим координатам
def check_winners_v2(f, cur_x, cur_y):
    cur_hand = f[cur_y][cur_x]
    len_f = len(f)
    # Проверка строк
    if f[cur_y].count(cur_hand) == len(f[cur_y]):
        return True
    # Проверка колонок
    if list(f[j][cur_x] for j in range(len_f)).count(cur_hand) == len_f:
        return True
    # Проверка диагонали \
    if cur_x - cur_y == 0:
        diagonal = list(f[i][i] for i in range(len_f))
        if diagonal.count(cur_hand) == len_f:
            return True
    # Проверка диагонали /
    if cur_x + cur_y == len_f - 1:
        diagonal = list(f[len_f - 1 - i][i] for i in range(len_f))
        if diagonal.count(cur_hand) == len_f:
            return True
    return False


def select_board():
    while True:
        size: str = input('Введите размер стороны квадрата (по умолчанию 3): ')
        if size == '':
            size = '3'
            break
        elif not (size.isdigit()):
            print('Введите цифры или пустую строку.')
            continue
        elif not (2 < int(size) < 11):
            print('Введите цифру больше 2 или меньше 11')
            continue
        break
    size: int = int(size)
    return size


def start_game():
    size_board = select_board()
    field = [['-'] * size_board for _ in range(size_board)]
    step = 0
    max_step = len(field) ** 2
    bot = None
    print('Играть c ботом? Пустая строка отказаться.')
    while bot not in {'x', 'o', ''}:
        bot = input('Выберите за что играет бот, x или o: ')
        if bot not in {'x', 'o', ''}:
            print('Введите пустую строку, x или o')
    coord_bot = gen_bot_coord(field, bot)
    # player = 'x' if bot != 'x' else 'o'
    # coord_player = gen_bot_coord(field, player)
    while True:
        if step == max_step:
            coord_bot.close()
            draw_game_board(field)
            print('Ничья')
            break
        hand = 'x' if step % 2 == 0 else 'o'
        print(f'Ход - {hand}')
        draw_game_board(field)
        if hand == bot:
            x, y = next(coord_bot)
            print(f'Координаты последнего хода - ({x}, {y})')
        else:
            x, y = input_coordinates(field)
            # x, y = next(coord_player)
            print(f'Координаты последнего хода - ({x}, {y})')
        field[y][x] = hand
        # check_winners(f, hand) or check_winners_v2(f, x, y)
        if step >= len(field) * 2 - 2 and check_winners_v2(field, x, y):
            coord_bot.close()
            draw_game_board(field)
            if bot == hand:
                print(f'Победил бот играя за {hand}')
            else:
                print(f'Вы победили играя за {hand}')
            break
        step += 1
    repeat = None
    while repeat not in {'y', 'n'}:
        repeat = input('Повторить (y/n): ')
        if repeat not in {'y', 'n'}:
            print('Введите y или n.')
    if repeat == 'y':
        return start_game()


start_game()
