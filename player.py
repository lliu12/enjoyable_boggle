import numpy as np
import boards

class Player(object):
    def __init__(self, skill, speed = 10, dictionary = boards.alphadict):
        self.skill = skill
        self.speed = speed # paths per second the player can check
        self.neighbors = np.array([
                        [0,1],
                        [1,0],
                        [0, -1],
                        [-1, 0],
                        [1, 1],
                        [-1, -1],
                        [1, -1],
                        [-1, 1],
                    ])
        self.dictionary = dictionary
        self.words_found = []
        self.steps_taken = 0
        self.steps_allowed = None

    # simulate gameplay
    def play(self, board, seconds = 120):
        self.words_found = []
        self.steps_allowed = self.speed * seconds
        self.steps_taken = 0

        board_indices = np.array(np.where(board)).T
        np.random.shuffle(board_indices)
        cur = 0
        while self.steps_taken < self.steps_allowed:
            pos = tuple(board_indices[cur])
            self.find_words_from(pos, board, '', [])
            cur = (cur + 1) % len(board_indices)

        return  list(set(self.words_found))

    # get neighboring tiles of a position
    def get_neighbors(self, board, pos):
        r,c = board.shape
        x,y = pos
        valid = []
        nbrs = self.neighbors + np.array(pos)
        for nbr in nbrs:
            if nbr[0] >= 0 and nbr[0] < r and nbr[1] >= 0 and nbr[1] < c:
                valid.append(nbr)
        return np.array(valid)

    # modified DFS from a position on the board
    def find_words_from(self, pos, board, prev_string, path):
        if self.steps_taken >= self.steps_allowed:
            return
        r,c = board.shape
        cur_string = prev_string + board[pos]
        path.append(pos)
        is_valid_word, prefix_freq = self.dictionary.is_word(cur_string)
        self.steps_taken += 1
        # determine if the player finds this word
        if is_valid_word and self.recognize_word(cur_string):
            self.words_found.append(cur_string)
        nbrs = self.get_neighbors(board, pos)
        # decide whether to keep searching neighbors
        if prefix_freq <= 0 or len(nbrs) <= 0 or not self.keep_searching(cur_string):
            return
        np.random.shuffle(nbrs)
        for nbr in nbrs:
            if (nbr[0], nbr[1]) not in path:
                self.find_words_from(tuple(nbr), board, cur_string, path.copy())

    # return true if the player recognizes this word
    def recognize_word(self, word):
        # chance that the player recognizes a word they see
        if len(word) <= 2 or word in self.words_found:
            return False
        length = len(word)
        prob = .8 ** (length) * (np.sqrt(self.skill))
        return np.random.random() < prob

    # return true if the player decides to keep searching along this path
    def keep_searching(self, word):
        isword, freq = self.dictionary.is_word(word)
        if freq >= 25:
            prob = .95 * np.sqrt((25 + 5 * self.skill) / 30)
            return np.random.random() < prob
        elif freq > 0:
            prob = .95 * np.sqrt((freq + 5 * self.skill) / 30)
            return np.random.random() < prob
        else:
            return False
