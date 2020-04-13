import anagram as angrm
import termcolor as termcolor
from termcolor import colored, cprint

if __name__ == '__main__':
    # Get the letters from the command line and return all anagrams.
    letters="komputer"
    
    board = [4, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 4, 5,
    0, 3, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 3, 0, 5,
    0, 0, 3, 0, 0, 0, 1, 0, 1, 0, 0, 0, 3, 0, 0, 5,
    1, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 1, 5,
    0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 5,
    0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 5,
    0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 5,
    4, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 4, 5,
    0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 5,
    0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 5,
    0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 5,
    1, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 1, 5,
    0, 0, 3, 0, 0, 0, 1, 0, 1, 0, 0, 0, 3, 0, 0, 5,
    0, 3, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 3, 0, 5,
    4, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 4] #This is the real board


    for word in angrm.anagram(letters, "words.txt"):
        print(word)