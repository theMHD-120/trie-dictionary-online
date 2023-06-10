class Node:
    def __init__(self, value):
        self.is_valid = False
        self.childs = [None for i in range(26)]
        self.value = value

    def __repr__(self):
        if self.is_valid:
            return f'*{self.value}*'
        return str(self.value)


class TrieDictionary:
    WORDS_PATH = 'words.txt'

    def __init__(self):
        self.root = Node('')
        self.read_words()

    def insert(self, word):
        this_root = self.root
        for c in word:
            if not this_root.childs[ord(c) - ord('a')]:
                this_root.childs[ord(c) - ord('a')] = Node(c)
            this_root = this_root.childs[ord(c) - ord('a')]
        this_root.is_valid = True

    def read_words(self):
        with open(TrieDictionary.WORDS_PATH) as file:
            words = [word.strip() for word in file.readlines()]
        for word in words:
            self.insert(word)
