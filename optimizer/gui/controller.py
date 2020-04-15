from pprint import pprint

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
        self.clear_layout()
        self._view.set_board(board)

    def clear_layout(self):
        if self._view.fieldsLayout is not None:
            while self._view.fieldsLayout.count():
                item = self._view.fieldsLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout()