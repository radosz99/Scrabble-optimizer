from pathlib import Path
import sys

def read_words(lang):
    #words = open('optimizer/resources/words'+lang+'.txt', "r")
    words = open(get_words(), "r")
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

def get_words():
    if getattr(sys, 'frozen', False):
        folder = Path(sys._MEIPASS)
    else:
        folder = Path(__file__).parent
    file = folder/'optimizer/resources/wordsPL.txt'
    return str(file)