from pprint import pprint
from PyQt5.QtCore import QThread, pyqtSignal
import random
import string
import time

class ScrabbleCntrl:
    def __init__(self, model, view):
        self._calculate = model
        self._view = view
        self.lang='ENG'
        self.scrabble_letters = self.get_list_of_chars(self.lang)
        # Connect signals and slots
        self._view.letter_remaining_lbl.setText(str(len(self.scrabble_letters)) + " letters remaining.")
        self.connect_signals()
        self._view.display.setText(self.randomString())

    def connect_signals(self):
        self._view.btn.clicked.connect(lambda: self.handle_click())
        self._view.btn_reset.clicked.connect(lambda: self.handle_reset_click())

    def add_letters(self, letters):
        for char in letters:
            self.scrabble_letters.append(char)
        print(str(len(self.scrabble_letters)) + " letters remaining")

#TODO handle whether too much letters are given
    def handle_click(self):
        self._view.btn.setText("Calculating...")
        self._view.btn.setEnabled(False)
        self.worker = AlgWorker(letters = self._view.get_letters(), board = self._view.get_board(), calculate=self._calculate, lang=self.lang)
        self.worker.end_signal.connect(self.end_signal_handle)        
        self.worker.start()                     

    def end_signal_handle(self, board, str_best, str_others, str_letters):
        self._view.btn.setText("Calculate for new letters")
        if(len(str_best)!=0):
            self._view.result_lbl.setText(str_best)
        else:
            self._view.result_lbl.setText("No words available!")
        self.clear_layout()
        self._view.set_board(board)
        self._view.btn.setEnabled(True)
        self.add_letters(str_letters)
        self._view.letter_remaining_lbl.setText(str(len(self.scrabble_letters)) + " letters remaining.")
        self._view.display.setText(self.randomString())
        self._view.other_result_lbl.setText("Other possible: " + str_others)
    
    def handle_reset_click(self):
        self._view.set_board(self._view.board_from_file)
        self.scrabble_letters.clear()
        self.scrabble_letters=self.get_list_of_chars(self.lang)
        self._view.letter_remaining_lbl.setText(str(len(self.scrabble_letters)) + " letters remaining.")
        self._view.display.setText(self.randomString())
        self._view.result_lbl.setText("")
        self._view.other_result_lbl.setText("")


    def clear_layout(self):
        if self._view.fieldsLayout is not None:
            while self._view.fieldsLayout.count():
                item = self._view.fieldsLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout()
    
    def randomString(self):
        string=''
        while(len(string)!=7 and len(self.scrabble_letters)!=0):
            index=random.randint(0,len(self.scrabble_letters)-1)
            char = self.scrabble_letters[index]
            string=string+char
            self.scrabble_letters.remove(char)

        return string

    
    def get_list_of_chars(self, lang):
        if(lang=='PL'):
            return ['a','a','a','a','a','a','a','a','a','e','e','e','e','e','e','e','i','i','i','i','i','i','i','i','n','n','n','n','n','o','o','o','o','o','o',
         'r','r','r','r','s','s','s','s','w','w','w','w','z','z','z','z','z','c','c','c','d','d','d','k','k','k','l','l','l','m','m','m','p','p','p','t','t','t','y','y','y','y',
         'b','b','g','g','h','h','j','j','ł','ł','u','u','ą','ę','f','ó','u','ś','ż','ć','ń','ź']
        elif(lang=='ENG'):
            return ['a','a','a','a','a','a','a','a','a','e','e','e','e','e','e','e','e','e','e','e','e','i','i','i','i','i','i','i','i','i','o','o','o','o','o','o','o','o',
        'n','n','n','n','n','n','r','r','r','r','r','r','t','t','t','t','t','t','l','l','l','l','s','s','s','s','u','u','u','u','d','d','d','d','g','g','g','b','b','c','c','m','m','p','p','f',
        'f','h','h','v','v','w','w','y','y','k','j','x','q','z']

class AlgWorker(QThread):
    end_signal = pyqtSignal(list, str, str, list)

    def __init__(self, letters, board, calculate,lang):
        super().__init__() 
        self.board = board
        self.letters = letters
        self.alg = calculate
        self.lang=lang

    def run(self):
        info = self.alg(self.letters, self.board, self.lang)
        board=info[0]
        best=info[1]
        others=info[2]
        letters_used=info[3]
        self.end_signal.emit(board, best, others,letters_used)
