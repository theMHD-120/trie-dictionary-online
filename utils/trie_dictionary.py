import os

UTILS_DIR = os.path.dirname(os.path.dirname(__file__))


class Node:
    def __init__(self, value):
        self.is_valid = False
        self.childs = [None for i in range(1026)]
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
        this_root = self.root
        for c in word:
            if not this_root.childs[ord(c) - ord('a')]:
                this_root.childs[ord(c) - ord('a')] = Node(c)
            this_root = this_root.childs[ord(c) - ord('a')]
        this_root.is_valid = True

    def __read_words(self):
        with open(TrieDictionary.WORDS_PATH) as file:
            words = [word.strip() for word in file.readlines()]
        for word in words:
            self.insert(word)

    def search_word(self, word):
        pass

    def make_suggestion(self, word):
        pass


trie_dict = TrieDictionary()
