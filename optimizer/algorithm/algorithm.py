from .anagram import find_anagrams

def algorithm_engine(letters,board):
    words = find_anagrams(letters)
    for y in range (len(words[len(words)-1])):
        board[3][y]=words[len(words)-1][y]
        
    new_board=[]
    for line in board:
        new_line=''
        for ch in line:
            new_line=new_line+str(ch)+';'
        new_board.append(new_line[0:len(new_line)-1])
        

    return new_board

