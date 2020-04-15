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
import sys
import time


class ScrabbleUi(QMainWindow):
    def __init__(self):
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
        board = [line.strip().lower() for line in f]

        self.set_board(board)

    def set_fields(self):
        for x in range(len(self._board)):
            for y in range(len(self._board[x])):
                self.fields[str(x)+';'+str(y)]=(x, y)
                
        for id, pos in self.fields.items():
            _id = id.split(';')
            label = QLabel(str(self._board[int(_id[0])][int(_id[1])]))
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

    def set_board(self,board):
        self._board=[]
        self._board.clear()
        for x in range(len(board)):
            self._board.append(board[x].split(";"))
        self.set_fields()
        
    def get_board(self):
        return self._board