import time

def read_words(lang):
    words = open("optimizer/resources/words"+lang+".txt", "r")
    return [line.strip().lower() for line in words]

def make_trie(lang):
    words = read_words(lang)
    root = {}
    for word in words:
        this_dict = root
        for letter in word:
            this_dict = this_dict.setdefault(letter, {})
        this_dict[None] = None
    return root