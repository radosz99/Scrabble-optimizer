from collections import Counter

def find_anagrams(letters, trie):
    letter_counts = Counter(letters)
    return anagram_engine(letter_counts, [], trie, len(letters))

def anagram_engine(letter_counts, path, root, word_length):
    words=[]
    if None in root.keys():
        word = ''.join(path)
        words.append(word)
    for letter, this_dict in root.items():
        count = letter_counts.get(letter, 0)
        if count == 0:
            continue
        letter_counts[letter] = count - 1
        path.append(letter)
        for word in anagram_engine(letter_counts, path, this_dict, word_length):
            words.append(word)
        path.pop()
        letter_counts[letter] = count
    return words