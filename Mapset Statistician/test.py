import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QCheckBox, QMainWindow, QWidget

class MyCheckBox(QCheckBox):
    def __init__(self,parent):
        super().__init__(parent)

        #Implement some additional functionality here

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300,300,300,300)
        self.wd = QWidget(self)
        self.wd.setGeometry(10,10,200,200)
        self.cb = MyCheckBox(self.wd)
        self.cb.setGeometry(10,10,100,40)
        self.cb.setText("Test")
        self.cb.setStyleSheet("""
                            QCheckBox {
                                width: 120px;
                                height: 60px;
                                background-color: #333333;
                                border-radius: 5px
                            }
                            """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.move(100,100)
    window.show()
    sys.exit(app.exec_())
