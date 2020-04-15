from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFrame
import optimizer.algorithm.anagram as angrm
from .algorithm.algorithm import algorithm_engine
from pprint import pprint
import sys
import time


class ScrabbleUi(QMainWindow):
    def __init__(self):
        """View initializer."""
        super().__init__()
        self.setWindowTitle("Scrabble Optimizer")
        self.setFixedSize(600, 600)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self.fieldsLayout = QGridLayout()
        self.create_display()
        self.create_button()
        self.create_fields()

    

    def create_display(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.generalLayout.addWidget(self.display)

    def create_button(self):
        self.btn = QPushButton('Calculate!')
        self.btn.setFixedHeight(35)
        self.generalLayout.addWidget(self.btn)

    def create_fields(self):
        self.fields = {}
        f = open("optimizer/resources/board.csv", "r")
        _board = [line.strip().lower() for line in f]

        self.set_board(_board)
        #self.set_fields()

    def set_fields(self):
        for x in range(len(self._new_board)):
            for y in range(len(self._new_board[x])):
                self.fields[str(x)+';'+str(y)]=(x, y)
                
        for id, pos in self.fields.items():
            _id = id.split(';')
            label = QLabel(str(self._new_board[int(_id[0])][int(_id[1])]))
            label.setFrameStyle(QFrame.Panel | QFrame.Raised)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold; color: red; font-size: 14")
            label.setUpdatesEnabled(True)
            self.fields[id] = label
            self.fields[id].setFixedSize(40, 40)
            self.fieldsLayout.addWidget(self.fields[id], pos[0], pos[1])
        self.generalLayout.addLayout(self.fieldsLayout)

    def get_letters(self):
        return self.display.text()

    def clear_letters(self):
        self.setDisplayText("")


    def clear_and_set_board(self, board):
        self.generalLayout.removeItem(self.fieldsLayout)
        self.set_board(board)

    def set_board(self,board):
        self._new_board=[]
        self._new_board.clear()
        for x in range(len(board)):
            self._new_board.append(board[x].split(";"))
        self.set_fields()
        
    def get_board(self):
        return self._new_board


def model_algorithm(letters, board):
    return algorithm_engine(letters,board)



class ScrabbleCntrl:
    def __init__(self, model, view):
        self._calculate = model
        self._view = view
        # Connect signals and slots
        self.connect_signals()

    def connect_signals(self):
        self._view.btn.clicked.connect(lambda: self.handle_click())

    def handle_click(self):
        board = self._calculate(letters = self._view.get_letters(), board = self._view.get_board())
        self._view.clear_and_set_board(board)
        


def run():
    app = QApplication([])
    view = ScrabbleUi()
    view.show()
    model = model_algorithm
    ScrabbleCntrl(view=view, model=model)
    sys.exit(app.exec_())
