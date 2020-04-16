from .anagram import find_anagrams
from ..trie.trie import make_trie

#TODO:evaluate move!!!

class Algorithm:
    def __init__(self, letters, board):
        self.letters = [x.lower() for x in letters]
        self.board = board
        self.create_patterns()

    def algorithm_engine(self):
        info_result = self.find_words()
        print(info_result)
        best = info_result[0]
        coords = info_result[1]

        if(coords[5]=='v'):
            for x in range (len(best)):
                self.board[coords[1]+x-coords[3]][coords[2]]=best[x]
        if(coords[5]=='h'):
            for x in range (len(best)):
                self.board[coords[1]][coords[2]+x-coords[3]]=best[x]

        result = 10
        new_board=[]
        for line in self.board:
            new_line=''
            for ch in line:
                new_line=new_line+str(ch)+';'
            new_board.append(new_line[0:len(new_line)-1])
               
        return new_board, result,best

    def find_words(self):
        ##--To trzeba bedzie wyliczyc na podstawie planszy
        ##---------------------------
        board_letters = 'akolwyprt'
        brigdes={'or':3,'lt':3}
        #----------------------------
        anagrams = find_anagrams(str(self.letters)+board_letters,make_trie())
        valid_anagrams = self.find_probably_valid_words(anagrams=anagrams, letters=str(self.letters), board_letters=board_letters, brigdes=brigdes)
        sorted_by_length = sorted(valid_anagrams, key=len)
        #print(sorted_by_length)
        counter=1
        word=''
        while(word==''):
            word_to_check=sorted_by_length[len(sorted_by_length)-counter]
            print(word_to_check)
            word = self.check_if_valid(word_to_check)
            counter=counter+1
    

        return word

    def check_if_valid(self,word):
        _word = word
        for char in self.letters:
            position = _word.find(char)
            if(position!=-1):
                help_word = _word[0 : position ] + _word[position + 1 : len(_word)]
                _word = help_word
            
        positions=[]
        if(len(_word)!=0):
            for char in _word:
                index = word.find(char)
                positions.append(index)
        else:
            return ''

        for pattern in self.pattern_board:
            if(str(pattern[0])==_word):
                if(len(_word)==2):
                    if(pattern[3]==positions[0]):
                        if(pattern[4]>(len(word)-positions[1]-1)):
                            return word, pattern
                if(len(_word)==1):
                    if(pattern[3]==positions[0]):
                        if(pattern[4]>(len(word)-positions[0]-1)):
                            return word, pattern
 
        return ''

    def find_probably_valid_words(self, anagrams, letters, board_letters, brigdes):
        max_letters_from_board_to_connect = 2 ##maksymalny most, czyli przewiduje max 2
        new_anagrams = []

        for anagram in anagrams:
            new_anagram=anagram
            _board_letters=board_letters
            whether_letter=False
            help_counter=0
            letters_find_in_both_place=[]
            for char in letters:
                index = new_anagram.find(char)
                #sprawdzenie czy znak znajduje sie w literach uzytkownika
                if(index!=-1): 
                    whether_letter=True
                    index_board = _board_letters.find(char)
                    #sprawdzenie czy znak znajduje sie w literach dostepnych na planszy, jesli tak to usuwany jest z dostepnych liter na planszy
                    if(index_board==-1):
                        help_anagram = new_anagram[0 : index ] + new_anagram[index + 1 : len(new_anagram)]
                        new_anagram = help_anagram
                    else:
                        letters_find_in_both_place.append(char)
                        help_counter=help_counter+1
                        help_board_letters = _board_letters[0 : index_board ] + _board_letters[index_board + 1 : len(_board_letters)]
                        _board_letters = help_board_letters
            #pierwszy warunek to, sprawdzenie czy w slowie jest wiecej niz 2 znaki spoza liter uzytkownika, czyli z planszy (mostek = 2 litery, kat prosty = 1 litera)
            #drugi warunek to sprawdzenie czy w slowie znajduja sie litery z planszy (jesli nie to string mialby dlugosc 0, czyli zawieral jedynie litery uzytkownika, co jest niedopuszczalne)
            #trzeci warunek to sprawdzenie czy zostala usunieta chociaz jedna literka (czyli, ze slowo zawiera chociaz jedna litere uzytkownika)
            if(len(new_anagram)<=max_letters_from_board_to_connect+help_counter and len(new_anagram)>0 and whether_letter==True):
                #usuniecie tych co znalazly sie w obu miejscach w celach walidacji
                if(anagram=='ubabram'):
                    print("Mam cie  " + new_anagram)
                for ch in letters_find_in_both_place:
                    index = new_anagram.find(ch)
                    if(index!=-1):
                        help_new_anagram = new_anagram[0 : index ] + new_anagram[index + 1 : len(new_anagram)]
                        new_anagram = help_new_anagram
                #sprawdzenie czy pasuje do mostkow
                if(anagram=='ubabram'):
                    print("Mam cie " + new_anagram)
                if(len(new_anagram)==2):
                    for key in brigdes:
                        if(new_anagram==key):
                            position1 = anagram.find(str(key)[0])
                            position2 = anagram.find(str(key)[1])
                            if(position2-position1==brigdes[key]):
                                new_anagrams.append(anagram)
                                break
                elif(len(new_anagram)<2):
                    new_anagrams.append(anagram)

        return(new_anagrams)
    
    #TODO:patterns shouldn't be hardcoded, solve it
    def create_patterns(self):
        self.pattern_board=[]
        self.pattern_board.append(('a', 5,5, 5,2, 'h'))
        self.pattern_board.append(('a', 5,5, 4,3, 'h'))
        self.pattern_board.append(('a', 5,5, 3,4, 'h'))
        self.pattern_board.append(('a', 5,5, 2,5, 'h'))
        self.pattern_board.append(('a', 5,5, 1,6, 'h'))
        self.pattern_board.append(('a', 5,5, 0,7, 'h'))
        self.pattern_board.append(('k', 7,1, 6,1, 'v'))
        self.pattern_board.append(('k', 7,1, 5,1, 'v'))
        self.pattern_board.append(('k', 7,1, 4,1, 'v'))
        self.pattern_board.append(('k', 7,1, 3,1, 'v'))
        self.pattern_board.append(('k', 7,1, 2,1, 'v'))
        self.pattern_board.append(('k', 7,1, 1,1, 'v'))
        self.pattern_board.append(('k', 7,1, 0,1, 'v'))
        self.pattern_board.append(('o', 7,2, 6,1, 'v'))
        self.pattern_board.append(('o', 7,2, 5,1, 'v'))
        self.pattern_board.append(('o', 7,2, 4,1, 'v'))
        self.pattern_board.append(('o', 7,2, 3,1, 'v'))
        self.pattern_board.append(('o', 7,2, 2,1, 'v'))
        self.pattern_board.append(('o', 7,2, 1,1, 'v'))
        self.pattern_board.append(('o', 7,2, 0,1, 'v'))
        self.pattern_board.append(('l', 7,3, 6,1, 'v'))
        self.pattern_board.append(('l', 7,3, 5,1, 'v'))
        self.pattern_board.append(('l', 7,3, 4,1, 'v'))
        self.pattern_board.append(('l', 7,3, 3,1, 'v'))
        self.pattern_board.append(('l', 7,3, 2,1, 'v'))
        self.pattern_board.append(('l', 7,3, 1,1, 'v'))
        self.pattern_board.append(('l', 7,3, 0,1, 'v'))
        self.pattern_board.append(('w', 7,7, 6,1, 'v'))
        self.pattern_board.append(('w', 7,7, 5,2, 'v'))
        self.pattern_board.append(('w', 7,7, 4,3, 'v'))
        self.pattern_board.append(('w', 7,7, 3,4, 'v'))
        self.pattern_board.append(('w', 7,7, 2,5, 'v'))
        self.pattern_board.append(('w', 7,7, 1,6, 'v'))
        self.pattern_board.append(('w', 7,7, 0,7, 'v'))
        self.pattern_board.append(('y', 7,8, 6,1, 'v'))
        self.pattern_board.append(('y', 7,8, 5,2, 'v'))
        self.pattern_board.append(('y', 7,8, 4,3, 'v'))
        self.pattern_board.append(('y', 7,8, 3,4, 'v'))
        self.pattern_board.append(('y', 7,8, 2,5, 'v'))
        self.pattern_board.append(('y', 7,8, 1,6, 'v'))
        self.pattern_board.append(('y', 7,8, 0,7, 'v'))
        self.pattern_board.append(('p', 9,5, 0,7, 'h'))
        self.pattern_board.append(('k', 10,0, 2,0, 'v'))
        self.pattern_board.append(('k', 10,0, 1,0, 'v'))
        self.pattern_board.append(('r', 10,2, 1,0, 'v'))
        self.pattern_board.append(('t', 10,3, 1,4, 'v'))
        self.pattern_board.append(('t', 10,3, 0,4, 'v'))
        self.pattern_board.append(('k', 10,4, 0,4, 'v'))
        self.pattern_board.append(('k', 12,1, 1,6, 'h'))
        self.pattern_board.append(('k', 12,1, 0,7, 'h'))
        self.pattern_board.append(('a', 13,1, 1,6, 'h'))
        self.pattern_board.append(('a', 13,1, 0,7, 'h'))
        self.pattern_board.append(('or', 7,2, 5,0, 'v',3))
        self.pattern_board.append(('or', 7,2, 4,0, 'v',3))
        self.pattern_board.append(('or', 7,2, 3,0, 'v',3))
        self.pattern_board.append(('or', 7,2, 2,0, 'v',3))
        self.pattern_board.append(('or', 7,2, 1,0, 'v',3))
        self.pattern_board.append(('or', 7,2, 0,0, 'v',3))
        self.pattern_board.append(('lt', 7,3, 0,4, 'v',3))
        self.pattern_board.append(('lt', 7,3, 1,3, 'v',3))
        self.pattern_board.append(('lt', 7,3, 2,2, 'v',3))
        self.pattern_board.append(('lt', 7,3, 3,1, 'v',3))
        self.pattern_board.append(('lt', 7,3, 4,0, 'v',3))