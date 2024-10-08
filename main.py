from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.uic import loadUi
from live_advance import LiveAdvance, your_app_client_id, your_app_client_secret, threshold, trained_profile_name #import the LiveAdvance class
from pynput.keyboard import Key, Controller
import time
kb = Controller()

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

        #passes in the current instance main_ui self into the LiveAdvance
        self.live_advance = LiveAdvance(self, your_app_client_id, your_app_client_secret) #create instance and pass self (UI) to it (added)

    def on_new_cmd(self, cmd): #cmd is the data coming from live_advance.py
        
        if self.is_processing_command == True:
            print(self.is_processing_command)
            return # Ignore new commands until the current one is processed
        print(self.is_processing_command)
        self.is_processing_command = True

        self.OutPutLabel.setText(f"Current Emotiv BCI output: {cmd['action']}, {cmd['power']}")

        self.simulate_key_press(cmd['action'], cmd['power'])

    def simulate_key_press(self, command, power):
        if command == 'push' and power >= threshold:
            selected_value = self.PushCombo.currentText() #set the selected value to be the text of that dropdown
        elif command == 'pull' and power >= threshold:
            selected_value = self.PullCombo.currentText()  # Get selected text from PullCombo dropdown
        elif command == 'left' and power >= threshold:
            selected_value = self.LeftCombo.currentText()  # Get selected text from LeftCombo dropdown
        elif command == 'right' and power >= threshold:
            selected_value = self.RightCombo.currentText()  # Get selected text from RightCombo dropdown
        else:
            selected_value = None

        if selected_value:
            #simulate the keyboard based on the selected value
            kb.press(selected_value.lower())
            print("Key pressed: ", selected_value)
            time.sleep(0.1) #only get the next mental command after the first push value is finished
            # Create a QTimer to release the key after 0.1 seconds
            # QtCore.QTimer.singleShot(100, lambda: self.release_key(selected_value.lower()))  # Release after 100 ms
            kb.release(selected_value.lower())

        #allow for a new mental command to be processed (put outside if statement so that neutral commands can be considered)
        self.is_processing_command = False


    #name is the box selected by the user and "value" is the new value they select from the drop down
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
        self.is_processing_command = False #initialize so that the first command can be processed
        self.live_advance.start(trained_profile_name)

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