from PyQt5.QtGui import QWindow


class MyPopup(QWindow):
    def __init__(self):
        QWindow.__init__(self)

    def paintEvent(self, e):
        dc = QPainter(self)
        dc.drawLine(0, 0, 100, 100)
        dc.drawLine(100, 0, 0, 100)
