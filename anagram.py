import sys
from collections import Counter

#Odczyt danych z pliku
def read_words(filename):
    return [line.strip().lower() for line in open(filename)]

#Zbudowanie struktury danych Trie zapewniającej niską złożoność operacji szukania
def make_trie(words):
    root = {}
    for word in words:
        this_dict = root
        for letter in word:
            this_dict = this_dict.setdefault(letter, {})
        this_dict[None] = None
    return root

def anagram(letters, dictionary):

    def _anagram(letter_counts, path, root, word_length):
        if None in root.keys():
            word = ''.join(path)
            yield word
        for letter, this_dict in root.items():
            count = letter_counts.get(letter, 0)
            if count == 0:
                continue
            letter_counts[letter] = count - 1
            path.append(letter)
            for word in _anagram(letter_counts, path, this_dict, word_length):
                yield word
            path.pop()
            letter_counts[letter] = count

    trie = make_trie(read_words(dictionary))
    letter_counts = Counter(letters)
    for word in _anagram(letter_counts, [], trie, len(letters)):
        yield word
