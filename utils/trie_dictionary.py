import os
from main.models import Word

UTILS_DIR = os.path.dirname(os.path.dirname(__file__))


class Node:
    """
    Nodes of trie
    """
    def __init__(self, value):
        self.is_valid = False
        self.childs = [None for i in range(130)]
        self.value = value

    def __repr__(self):
        if self.is_valid:
            return f'*{self.value}*'
        return str(self.value)


class TrieDictionary:
    """
    Trie Dictionary
    this has 2 initial nodes
    one for true words and another for reversed words
    """
    WORDS_PATH = str(os.path.join(UTILS_DIR, 'utils\\words.txt'))

    def __init__(self):
        """
        initialize trie
        reading from words.txt file
        """
        self.root = Node('')
        self.inv_root = Node('')
        self.__read_words()

    def save_to_db(self, word):
        """
        saves the given word to database.
        """
        new_word = Word.objects.create(word=word)
        new_word.save()
        return True

    def delete_from_db(self, word):
        """
        deletes word from database.
        """
        all_word_objects = Word.objects.all()
        for word_obj in all_word_objects:
            if word_obj.word == word:
                word_obj.delete()

    def __read_words(self):
        """
        reads words from files and inserts it to trie
        """
        with open(TrieDictionary.WORDS_PATH, 'r') as file:
            words = [word.strip() for word in file.readlines()]
        for word in words:
            if word == '---':
                continue
            self.insert_to_trie(word, start_node=self.root)
            self.insert_to_trie(word[::-1], start_node=self.inv_root)

    def insert_to_trie(self, word, start_node):
        """
        inserts words to trie
        """
        already_exists = self.search_word(word, start_node)
        if not already_exists:
            this_node = start_node
            for char in word:
                if not this_node.childs[ord(char) - 32]:
                    this_node.childs[ord(char) - 32] = Node(char)
                this_node = this_node.childs[ord(char) - 32]
            this_node.is_valid = True
            return True
        return False

    def add_new_word(self, word):
        """
        adds new word to trie if it is not exists
        """
        res = self.insert_to_trie(word, self.root)
        self.insert_to_trie(word[::-1], self.inv_root)
        if res:
            self.save_to_db(word)
            with open(TrieDictionary.WORDS_PATH, 'a') as file:
                file.write('---\n')
                file.write(word + '\n')
            return True
        return False

    def search_word(self, word, start_node, make_suggestion=False):
        """
        search for a word in trie
        if it existed returns True
        if not returns a list of suggestions
        """
        this_node = start_node
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
            # if word not found in trie first try to find autocompletes
            suggestions = self.auto_complete(word)
            # after autocomplete, try to make suggestions.
            if suggestions:
                suggestions = suggestions
            else:
                suggestions = self.get_suggestions(word, suggestions)
            return suggestions
        return found

    def get_last_node(self, word, start_node):
        """
        finds last common node between trie and given word
        """
        this_node = start_node
        i = 0
        while True:
            if this_node.childs[ord(word[i]) - 32]:
                if this_node.childs[ord(word[i]) - 32].value == word[i]:
                    this_node = this_node.childs[ord(word[i]) - 32]
                    if i == len(word) - 1:
                        return this_node, i
                    i += 1
            else:
                return this_node, i

    def find_results(self, last_node, last_pre, all_results, reverse=False):
        """
        finds suggestions, starts with the last common node recursively.
        """
        if last_node.is_valid and last_pre not in all_results:
            if reverse:
                all_results.append(last_pre[::-1])
            else:
                all_results.append(last_pre)
        for n in last_node.childs:
            pre = last_pre
            if n:
                pre += n.value
                if reverse:
                    self.find_results(n, pre, all_results, True)
                else:
                    self.find_results(n, pre, all_results)

    def auto_complete(self, word):
        """
        auto completes invalid word
        """
        last_node, first_different_index = self.get_last_node(word, self.root)
        if last_node and last_node.value == word[first_different_index]:
            all_results = []
            self.find_results(last_node, word, all_results)
            return all_results
        return None

    def get_suggestions(self, word, suggests):
        """
        if word is not valid guesses some suggests instead of word
        """

        # if word be prefix ...
        last_node, first_different_index = self.get_last_node(word, self.root)
        if last_node and last_node != self.root:
            if not suggests:
                suggests = []
                sub_word = word[:first_different_index]
            else:
                sub_word = word[:first_different_index + 1]
            self.find_results(last_node, sub_word, suggests)

        #  if word be suffix ...
        last_inv_node, first_different_inv_index = self.get_last_node(word[::-1], self.inv_root)
        word = word[::-1]
        if last_inv_node and last_inv_node != self.inv_root:
            if not suggests:
                suggests = []
            sub_inv_word = word[:first_different_inv_index]
            self.find_results(last_inv_node, sub_inv_word, suggests, True)

        return suggests


trie_dict = TrieDictionary()