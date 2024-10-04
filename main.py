from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.uic import loadUi


class WelcomeScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("MainWindow.ui", self)
        self.StartButton.clicked.connect(lambda: self.start_mapping())
        self.PauseButton.clicked.connect(lambda: self.pause_mapping())
        self.PullCombo.currentIndexChanged.connect(lambda: self.on_combobox_changed('pull', self.PullCombo.currentIndex()))
        self.PushCombo.currentIndexChanged.connect(lambda: self.on_combobox_changed('push', self.PushCombo.currentIndex()))
        self.LeftCombo.currentIndexChanged.connect(lambda: self.on_combobox_changed('left', self.LeftCombo.currentIndex()))
        self.RightCombo.currentIndexChanged.connect(lambda: self.on_combobox_changed('right', self.RightCombo.currentIndex()))

    def on_new_cmd(self, cmd):
        self.OutPutLabel.setText(f"Current Emotiv BCI output: {cmd['action']}, {cmd['power']}")

    def on_combobox_changed(self, name, value):
        if name == 'push':
            print(value)
        elif name == 'pull':
            print(value)
        elif name == 'left':
            print(value)
        elif name == 'right':
            print(value)

    def start_mapping(self):
        print('start_mapping')

    def pause_mapping(self):
        print('pause mapping')


app = QtWidgets.QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setWindowIcon(QtGui.QIcon("logo.png")) #add a logo here
widget.setWindowTitle("Emotiv DJI Controller")
widget.resize(796,349)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")