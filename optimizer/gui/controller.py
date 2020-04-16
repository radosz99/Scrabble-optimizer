from pprint import pprint
from multiprocessing.pool import ThreadPool
from PyQt5.QtCore    import QThread, pyqtSignal

class ScrabbleCntrl:
    def __init__(self, model, view):
        self._calculate = model
        self._view = view
        # Connect signals and slots
        self.connect_signals()
        

    def connect_signals(self):
        self._view.btn.clicked.connect(lambda: self.handle_click())

    def handle_click(self):
        self._view.btn.setText("Calculating...")
        self._view.btn.setEnabled(False)
        self.worker = AlgWorker(letters = self._view.get_letters(), board = self._view.get_board(), _calculate=self._calculate)
        self.worker.finishSignal.connect(self.on_finishSignal)        
        self.worker.start()                     

    def on_finishSignal(self, board):
        self._view.btn.setText("Calculate for new letters")
        self.clear_layout()
        self._view.set_board(board)
        self._view.btn.setEnabled(True)

    def clear_layout(self):
        if self._view.fieldsLayout is not None:
            while self._view.fieldsLayout.count():
                item = self._view.fieldsLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout()

class AlgWorker(QThread):
    finishSignal = pyqtSignal(list)

    def __init__(self, letters, board, _calculate):
        super().__init__() 
        self.board = board
        self.letters = letters
        self.alg = _calculate

    def run(self):
        board = self.alg(self.letters, self.board)
        QThread.msleep(500)
        self.finishSignal.emit(board)
