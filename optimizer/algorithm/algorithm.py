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
        points = info_result[1]
        best = info_result[0][0]
        coords = info_result[0][1]

        if(coords[5]=='v'):
            for x in range (len(best)):
                if(x!=coords[3]):
                    self.board[coords[1]+x-coords[3]][coords[2]]=best[x]
        if(coords[5]=='h'):
            for x in range (len(best)):
                if(x!=coords[3]):
                    self.board[coords[1]][coords[2]+x-coords[3]]=best[x]
        new_board=[]
        for line in self.board:
            new_line=''
            for ch in line:
                new_line=new_line+str(ch)+';'
            new_board.append(new_line[0:len(new_line)-1])
               
        return new_board, points,best

    def find_words(self):
        ##--To trzeba bedzie wyliczyc na podstawie planszy
        ##---------------------------
        board_letters = 'akolwyprt'
        brigdes={'or':3,'lt':3}
        #----------------------------
        anagrams = find_anagrams(str(self.letters)+board_letters,make_trie())
        valid_anagrams = self.find_probably_valid_words(anagrams=anagrams, letters=str(self.letters), board_letters=board_letters, brigdes=brigdes)
        sorted_by_length = sorted(valid_anagrams, key=len)
        counter=1
        word=''
        list_of_valid_words=[]

        while(counter!=len(sorted_by_length)-1):
            word_to_check=sorted_by_length[len(sorted_by_length)-counter]
            word = self.check_if_valid(word_to_check)     
            if(word!=''):
                result = self.evaluate_move(word)
                list_of_valid_words.append((word,result))
            counter=counter+1

        sorted_list_of_valid_words = sorted(list_of_valid_words, key=lambda tup: tup[1])
        result = sorted_list_of_valid_words[len(sorted_list_of_valid_words)-1]

        return result

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
                for ch in letters_find_in_both_place:
                    index = new_anagram.find(ch)
                    if(index!=-1):
                        help_new_anagram = new_anagram[0 : index ] + new_anagram[index + 1 : len(new_anagram)]
                        new_anagram = help_new_anagram
                #sprawdzenie czy pasuje do mostkow
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

    def evaluate_move(self, word_with_pattern):
        coords = word_with_pattern[1]
        word = word_with_pattern[0]
        sum=0
        multiplier=1
        if(coords[5]=='v'):
            for x in range (len(word)):
                if(len(coords[0])==2):
                    if(x!=coords[3] and x!=(coords[3]+coords[6])):
                        info = self.get_field_value(word[x], coords[1]+x-coords[3],coords[2])
                        sum=sum+int(info[0])
                        multiplier=int(multiplier*int(info[1]))
                else:
                    if(x!=coords[3]):
                        info = self.get_field_value(word[x], coords[1]+x-coords[3],coords[2])
                        sum=sum+int(info[0])
                        multiplier=int(multiplier*int(info[1]))

        if(coords[5]=='h'):
            for x in range (len(word)):
                if(len(coords[0])==2):
                    if(x!=coords[3] and x!=(coords[3]+coords[6])):
                        info = self.get_field_value(word[x], coords[1],coords[2]+x-coords[3])
                        sum=sum+int(info[0])
                        multiplier=int(multiplier*int(info[1]))
                else:
                    if(x!=coords[3]):
                        info = self.get_field_value(word[x], coords[1],coords[2]+x-coords[3])
                        sum=sum+int(info[0])
                        multiplier=int(multiplier*int(info[1]))
        return sum*multiplier
                        


    def get_field_value(self, char, x,y):
        word_multiplier=1
        letter_multiplier=1
        letter_value = self.get_char_value(char)
        if(((x==1 or x==13)and (y==1 or y==13)) or ((x==2 or x==12) and (y==2 or y==12)) or ((x==3  or x==11) and (y==3 or y==11)) or ((x==4 or x==10) and (y==4 or y==10))):
            word_multiplier=2
        if(((x==0 or x==14) and (y==0 or y==7 or y==14)) or (x==7 and (y==0 or y==14))):
            word_multiplier=3

        if(((x==5 or x==9) and (y==1 or y==5 or y==9 or y==13)) or ((x==1 or x==13) and (y==5 or y==9))):
            letter_multiplier=3
        if(((x==0 or x==7 or x==14) and (y==3 or y==11)) or ((x==3 or x==11) and (y==0 or y==7 or y==14))
            or((x==2 or x==6 or x==8 or x==12) and (y==6 or y==8)) or((y==2 or y==6 or y==8 or y==12) and (x==6 or x==8))):
            letter_multiplier=2
        if(x==7 and y==7):
            letter_multiplier=1
            word_multiplier=1

        return letter_multiplier*letter_value, word_multiplier

    def get_char_value(self,char):
        if(char=='a' or char=='e' or char=='i' or char=='n' or char=='o' or char=='r' or char=='s' or char=='w' or char=='z'):
            return 1
        if(char=='c' or char=='d' or char=='k' or char=='l' or char=='m' or char=='p' or char=='t' or char=='y'):
            return 2
        if(char=='b' or char=='g' or char=='h' or char=='j' or char=='ł' or char=='u'):
            return 3
        if(char=='ą' or char=='ę' or char=='f' or char=='ó' or char=='ś' or char=='ż'):
            return 5
        if(char=='ć'):
            return 6
        if(char=='ń'):
            return 7
        if(char=='ź'):
            return 9
        return 1