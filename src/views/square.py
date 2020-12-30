from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor, QPalette
from PyQt5.Qt import Qt


class Square(QPushButton):
    def __init__(self, pos, sz):
        super(Square, self).__init__('')  # , flat=True)
        self.pos = pos
        self.setMinimumWidth(sz)
        self.setMinimumHeight(sz)
        # self.resize(sz, sz)
        # self.setGeometry(0, 0, sz, sz)
        self.clicked.connect(self.mouse_clicked)
        # palette = self.palette()
        # palette.setColor(QPalette.Inactive, QPalette.Window, Qt.transparent)

    def mouse_clicked(self):
        print(str(self.pos) + " clicked")
