import sys
from .gui.controller import ScrabbleCntrl
from .gui.view import ScrabbleUi
from PyQt5.QtWidgets import QApplication
from .gui.model import model_algorithm

def run():
    app = QApplication([])
    view = ScrabbleUi()
    view.show()
    ScrabbleCntrl(view=view, model=model_algorithm)
    sys.exit(app.exec_())
