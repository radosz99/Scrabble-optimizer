from .anagram import find_anagrams
from ..trie.trie import make_trie

class Algorithm:
    def __init__(self, letters, board):
        self.letters = letters
        self.board = board

    def algorithm_engine(self):
        anagrams = find_anagrams(self.letters,make_trie())

        for y in range (len(anagrams[len(anagrams)-1])):
            self.board[3][y]=anagrams[len(anagrams)-1][y]
            
        new_board=[]
        for line in self.board:
            new_line=''
            for ch in line:
                new_line=new_line+str(ch)+';'
            new_board.append(new_line[0:len(new_line)-1])
            

        return new_board

