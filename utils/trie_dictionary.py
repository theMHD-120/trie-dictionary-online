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

    def __read_words(self):
        with open(TrieDictionary.WORDS_PATH, 'r') as file:
            words = [word.strip() for word in file.readlines()]
        for word in words:
            if word == '---':
                continue
            self.insert_to_trie(word)

    def insert_to_trie(self, word):
        already_exists = self.search_word(word)
        if not already_exists:
            this_node = self.root
            for char in word:
                if not this_node.childs[ord(char) - 32]:
                    this_node.childs[ord(char) - 32] = Node(char)
                this_node = this_node.childs[ord(char) - 32]
            this_node.is_valid = True
            return True
        return False

    def add_new_word(self, word):
        res = self.insert_to_trie(word)
        if res:
            with open(TrieDictionary.WORDS_PATH, 'a') as file:
                file.write('---\n')
                file.write(word + '\n')
            return True
        return False

    def search_word(self, word, make_suggestion=False):
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
        if not found and make_suggestion:
            suggestions = self.auto_complete(word)
            self.get_suggestion(word, suggestions)
            if suggestions:
                suggestions = suggestions[:5]
            return suggestions
        return found

    def get_last_node(self, word):
        this_node = self.root
        i = 0
        while True:
            if this_node.childs[ord(word[i]) - 32]:
                if this_node.childs[ord(word[i]) - 32].value == word[i]:
                    this_node = this_node.childs[ord(word[i]) - 32]
                    if i == len(word) - 1:
                        return this_node
                    i += 1
            else:
                return False

    def find_results(self, last_node, last_pre, all_results):
        if last_node.is_valid:
            all_results.append(last_pre)
        for n in last_node.childs:
            pre = last_pre
            if n:
                pre += n.value
                self.find_results(n, pre, all_results)

    def auto_complete(self, word):
        last_node = self.get_last_node(word)
        if last_node:
            all_results = []
            self.find_results(last_node, word, all_results)
            return all_results
        return None

    def get_suggestion(self, word, suggests):
        pass


trie_dict = TrieDictionary()