from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor, QPalette
from PyQt5.Qt import Qt


class Square(QPushButton):
    def __init__(self, pos):
        super(Square, self).__init__('', flat=True)
        self.pos = pos
        # self.resize(40, 12)
        self.clicked.connect(self.mouse_clicked)
        palette = self.palette()
        palette.setColor(QPalette.Inactive, QPalette.Window, Qt.transparent)

    def mouse_clicked(self):
        print(str(self.pos) + " clicked")
