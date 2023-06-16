import os

UTILS_DIR = os.path.dirname(os.path.dirname(__file__))


class Node:
    def __init__(self, value):
        self.is_valid = False
        self.childs = [None for i in range(130)]
        self.value = value

    def __repr__(self):
        if self.is_valid:
            return f'*{self.value}*'
        return str(self.value)


class TrieDictionary:
    WORDS_PATH = str(os.path.join(UTILS_DIR, 'utils\\words.txt'))

    def __init__(self):
        self.root = Node('')
        self.__read_words()

    def insert(self, word):
        this_node = self.root
        for c in word:
            if not this_node.childs[ord(c) - 32]:
                this_node.childs[ord(c) - 32] = Node(c)
            this_node = this_node.childs[ord(c) - 32]
        this_node.is_valid = True

    def __read_words(self):
        with open(TrieDictionary.WORDS_PATH) as file:
            words = [word.strip() for word in file.readlines()]
        for word in words:
            self.insert(word)

    def search_word(self, word):
        this_node = self.root
        index = 0
        found = False
        finished = False
        while not finished:
            node = this_node.childs[ord(word[index]) - 32]
            if node and node.value == word[index]:
                index += 1
                this_node = node
                if index == len(word):
                    if this_node.is_valid:
                        found = True
                        finished = True
                    else:
                        finished = True
            else:
                finished = True
        return found

    def make_suggestion(self, word):
        pass


trie_dict = TrieDictionary()
