# implementation of trie for use in Boggle board generation project

# A Node object
class Node(object):
    def __init__(self, char):
        self.char = char
        self.children = {}
        self.word = False
        self.freq = 1

# A Trie
class Trie(object):
    def __init__(self, words = []):
        self.root = Node("")
        for word in words:
            self.add(word)

    # Add a word to the trie
    def add(self, word):
        node = self.root
        # For each letter in the word, add a node if necessary
        for char in word:
            if char in node.children:
                node = node.children[char]
                node.freq += 1
            else:
                new = Node(char)
                node.children[char] = new
                node = new
        # Mark node for last letter as end of a word
        node.word = True

    def is_word(self, word):
        node = self.root
        found = True
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                found = False
                return False, 0
        # to be a word, you must be found in the tree & end at a node marked as "end of word"
        return found and node.word, node.freq

  