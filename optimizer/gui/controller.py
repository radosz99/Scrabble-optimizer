from pprint import pprint
from PyQt5.QtCore import QThread, pyqtSignal
import random
import string

class ScrabbleCntrl:
    def __init__(self, model, view):
        self._calculate = model
        self._view = view
        # Connect signals and slots
        self.connect_signals()
        
    def connect_signals(self):
        self._view.btn.clicked.connect(lambda: self.handle_click())
        self._view.btn_reset.clicked.connect(lambda: self.handle_reset_click())

#TODO handle whether too much letters are given
    def handle_click(self):
        self._view.btn.setText("Calculating...")
        self._view.btn.setEnabled(False)
        self.worker = AlgWorker(letters = self._view.get_letters(), board = self._view.get_board(), calculate=self._calculate)
        self.worker.end_signal.connect(self.end_signal_handle)        
        self.worker.start()                     

    def end_signal_handle(self, board, result, word):
        self._view.btn.setText("Calculate for new letters")
        if(len(word)!=0):
            self._view.result_lbl.setText("Played '" + word + "' for " + result + " points")
        else:
            self._view.result_lbl.setText("No words available!")
        self.clear_layout()
        self._view.set_board(board)
        self._view.btn.setEnabled(True)
        self._view.display.setText(self.randomString())
    
    def handle_reset_click(self):
        self._view.set_board(self._view.board_from_file)


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
        letters = ['a','a','a','a','a','a','a','a','a','e','e','e','e','e','e','e','i','i','i','i','i','i','i','i','n','n','n','n','n','o','o','o','o','o','o',
        'r','r','r','r','s','s','s','s','w','w','w','w','z','z','z','z','z','c','c','c','d','d','d','k','k','k','l','l','l','m','m','m','p','p','p','t','t','t','y','y','y','y',
        'b','b','g','g','h','h','j','j','ł','ł','u','u','ą','ę','f','ó','u','ś','ż','ć','ń','ź']
        return ''.join(random.choice(letters) for i in range(7))

class AlgWorker(QThread):
    end_signal = pyqtSignal(list, str, str)

    def __init__(self, letters, board, calculate):
        super().__init__() 
        self.board = board
        self.letters = letters
        self.alg = calculate

    def run(self):
        info = self.alg(self.letters, self.board)
        board=info[0]
        result=str(info[1])
        best=info[2]
        self.end_signal.emit(board, result, best)
