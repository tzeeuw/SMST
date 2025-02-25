from smst.server.base_server import base_server
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import *
import sys
import threading
import json


with open('properties.json', 'r') as file:
    properties = json.load(file)



class mcgui(QtWidgets.QMainWindow):
    def __init__(self, size=(1600, 900)):
        super().__init__()
        window_center = QtGui.QGuiApplication.primaryScreen().size().toTuple()

        #TODO: make command and directory not required for handler
        directory = properties["cwd"]
        command = properties["cmd"]
        self.server = base_server(cmd=command, cwd=directory)




        #self.setGeometry(QRect(QPoint(780, 470), QSize(*size)))
        self.setGeometry(QRect(QPoint((window_center[0]-size[0])/2, (window_center[1]-size[1])/2), QSize(*size)))
        self.init_layout()
        self.init_widgets()
        self.init_menubar()
        self.add_layout()
        

    def init_widgets(self):
        self.start_button = QtWidgets.QPushButton("start")
        self.start_button.clicked.connect(self.start_server)

        self.stop_button = QtWidgets.QPushButton("stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_server)

        self.terminal_text = QtWidgets.QTextEdit()
        self.terminal_text.setText("Test")
        self.terminal_text.setReadOnly(True)

        self.input_box = QtWidgets.QLineEdit()
        self.input_box.installEventFilter(self)


    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.input_box:
            if event.key() == Qt.Key_Return and self.input_box.hasFocus():
                self.server.input_handling(self.input_box.text())
                print("test") 
                self.input_box.clear()
            
        return super().eventFilter(obj, event)
    



    def init_menubar(self):
        self.menu_bar = QtWidgets.QMenuBar()
        self.menu = QtWidgets.QMenu("test")
        
        self.menu_bar.addMenu(self.menu)
        self.setMenuBar(self.menu_bar)

    def init_layout(self):
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.hbox_central = QtWidgets.QHBoxLayout(self.central_widget)

        self.hbox_buttons = QtWidgets.QHBoxLayout()
        self.hbox_central.addLayout(self.hbox_buttons)

        self.vbox_text = QtWidgets.QVBoxLayout()
        self.hbox_central.addLayout(self.vbox_text)

    def add_layout(self):
        self.hbox_buttons.addWidget(self.start_button)
        self.hbox_buttons.addWidget(self.stop_button)

        self.vbox_text.addWidget(self.terminal_text)
        self.vbox_text.addWidget(self.input_box)


    #TODO: fix jumping of scrollbar
    def update_text(self):

        prev_value = self.terminal_text.verticalScrollBar().value()

        lines = "\n".join(self.server.lines)
        self.terminal_text.setText(lines)

        self.terminal_text.ensureCursorVisible()
        self.terminal_text.verticalScrollBar().setSliderPosition(prev_value)




    def start_server(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.timer.start(10)


        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.server.start_server()



    def stop_server(self):
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.server.stop_server()

    



if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv + ['-platform', 'windows:darkmode=2'])
    app.setStyle("Fusion")


    window = mcgui(size=(1200, 1200/16*9))

    window.show()
    sys.exit(app.exec())


