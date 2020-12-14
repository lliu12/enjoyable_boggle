import numpy as np
from trie import Node, Trie

# build Trie
dict_words = np.loadtxt("smaller_dict.txt", dtype = str)
alphadict = Trie(dict_words)

# dictionary of letters
alphabet = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h',
    8: 'i',
    9: 'j',
    10: 'k',
    11: 'l',
    12: 'm',
    13: 'n',
    14: 'o',
    15: 'p',
    16: 'q',
    17: 'r',
    18: 's',
    19: 't',
    20: 'u',
    21: 'v',
    22: 'w',
    23: 'x',
    24: 'y',
    25: 'z'
}

# uniform distribution
unif = {}
for i in range(26):
    unif[i] = 1/26
    
# english distribution
# frequencies from http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
eng = {
    4: .1202,
    19: .0910,
    0: .0812,
    14: .0768,
    8: .0731,
    13: .0695,
    18: .0628,
    17: .0602,
    7: .0592,
    3: .0432,
    11: .0398,
    20: .0288,
    2: .0271,
    12: .0261,
    5: .0230,
    24: .0211,
    22: .0209,
    6: .0203,
    15: .0182,
    1: .0149,
    21: .0111,
    10: .0069,
    23: .0017,
    16: .0011,
    9: .0010,
    25: .0007
}

# draw a letter from a distribution
def draw_letter(dist):
    x = np.random.uniform()
    ctr = 0
    for i in range(26):
        if ctr + dist[i] > x:
            letter = alphabet[i]
            return letter
        else:
            ctr += dist[i]
    return draw_letter(dist)

# generate board by pulling each tile randomly from a given alphabet distribution
def gen_board_dist(dist, rows = 4, cols = 4):
    board = np.empty((rows, cols), dtype = object)
    for i in range(rows):
        for j in range(cols):
            board[i][j] = draw_letter(dist)
    return board

# boggle english dice configs 
# https://boardgames.stackexchange.com/questions/29264/boggle-what-is-the-dice-configuration-for-boggle-in-various-languages
dice = np.array([
    ['r', 'i', 'f', 'o', 'b', 'x'], # dice 0 faces
    ['i', 'f', 'e', 'h', 'e', 'y'], # dice 1 faces
    ['d', 'e', 'n', 'o', 'w', 's'], # ...
    ['u', 't', 'o', 'k', 'n', 'd'],
    ['h', 'm', 's', 'r', 'a', 'o'],
    ['l', 'u', 'p', 'e', 't', 's'],
    ['a', 'c', 'i', 't', 'o', 'a'],
    ['y', 'l', 'g', 'k', 'u', 'e'],
    ['q', 'b', 'm', 'j', 'o', 'a'],
    ['e', 'h', 'i', 's', 'p', 'n'],
    ['v', 'e', 't', 'i', 'g', 'n'],
    ['b', 'a', 'l', 'i', 'y', 't'],
    ['e', 'z', 'a', 'v', 'n', 'd'],
    ['r', 'a', 'l', 'e', 's', 'c'],
    ['u', 'w', 'i', 'l', 'r', 'g'],
    ['p', 'a', 'c', 'e', 'm', 'd'],
])

# generate a board using the die rolling method
def gen_board_dice(rows = 4, cols = 4, dice = dice):
    np.random.shuffle(dice)
    board = np.empty((rows, cols), dtype = object)
    ct = 0
    for i in range(rows):
        for j in range(cols):
            board[i][j] = np.random.choice(dice[ct])    
            ct += 1
    return board

# possible neighbor directions
neighbors = np.array([
    [0,1],
    [1,0],
    [0, -1],
    [-1, 0],
    [1, 1],
    [-1, -1],
    [1, -1],
    [-1, 1],
])

# given a position on a board, return the board positions that are empty neighbors of it
def get_empty_neighbors(board, pos, neighbors = neighbors):
    r,c = board.shape
    x,y = pos
    valid = []
    nbrs = neighbors + np.array(pos)
    for nbr in nbrs:
        if nbr[0] >= 0 and nbr[0] < r and nbr[1] >= 0 and nbr[1] < c:
            if board[nbr[0], nbr[1]] == '':
                valid.append(nbr)
    return np.array(valid)

# generate board using seeding algorithm
def gen_board_seed(rows = 4, cols = 4, words = dict_words):
    board = np.full((rows, cols), '', dtype = object)
    while len(np.where(board == '')[0]) > 0:
        empty = np.where(board == '')
        w = np.random.choice(words)
        r = np.random.randint(0, len(empty[0])) # choose location on board to start word at
        x, y = empty[0][r], empty[1][r]
        # fill in path until word is done or no other empty neighbors left
        for l in w:
            board[x][y] = l
            neighbors = get_empty_neighbors(board, np.array([x,y]))
            if len(neighbors) <= 0:
                break
            next_id = np.random.randint(0, len(neighbors))
            x,y = neighbors[next_id][0], neighbors[next_id][1]
#         print(board)
    return board

# get all neighbors of a board position
def get_neighbors(board, pos, neighbors = neighbors):
    r,c = board.shape
    x,y = pos
    valid = []
    nbrs = neighbors + np.array(pos)
    for nbr in nbrs:
        if nbr[0] >= 0 and nbr[0] < r and nbr[1] >= 0 and nbr[1] < c:
            valid.append(nbr)
    return np.array(valid)

# run DFS from a particular position
def find_words_from(pos, board, dictionary, prev_string, path, board_words, neighbors = neighbors):
    r,c = board.shape
    cur_string = prev_string + board[pos]
    path.append(pos)
    is_valid_word, prefix_freq = dictionary.is_word(cur_string)
    # check if word in dictionary
    if is_valid_word and len(cur_string) > 2:
        board_words.append(cur_string)
    nbrs = get_neighbors(board, pos)
    # prune path tree using frequency in prefix tree
    if prefix_freq <= 0 or len(nbrs) <= 0:
        return
    for nbr in nbrs:
        if (nbr[0], nbr[1]) not in path:
            # run DFS on neighbor
            find_words_from(tuple(nbr), board, dictionary, cur_string, path.copy(), board_words)

# fully search board for words
def search_board(board, dictionary):
    board_words = []
    r,c = board.shape
    for i in range(r):
        for j in range(c):
            find_words_from((i,j), board, dictionary, '', [], board_words)
    return list(set(board_words))