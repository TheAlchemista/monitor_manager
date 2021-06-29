import sys
from pprint import pprint
from PySide6 import QtCore, QtWidgets, QtGui

# Project imports
from Get_Setup import Get_Setup
from Button import Button, Exit_Button


class MainWidget(QtWidgets.QWidget):
    def __init__(self, labels, buttons, exit_button):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.labels = labels
        self.buttons = buttons
        self.exit_button = exit_button
        self.add_content()
    
    def add_content(self):
        for label, button in zip(self.labels, self.buttons):
            self.layout.addWidget(label)
            self.layout.addWidget(button.get_button())
            self.layout.addWidget(self.exit_button)


class Monitor:
    def __init__(self, config):
        self.state = True
        self.config = config

    def set_turned_off(self):
        self.config["State"] = 'off'

    def set_turned_on(self):
        self.config["State"] = 'on'


class App:
    def __init__(self):
        self.setup = Get_Setup()

        self.app = QtWidgets.QApplication([])

        self.monitors = self.get_monitors()
        self.buttons = self.get_buttons()
        self.labels = self.create_labels()

        self.widget = MainWidget(self.labels, self.buttons, Exit_Button())
        self.widget.setWindowTitle("Turn monitors on and off")
        self.widget.resize(700, 400)
        self.widget.show()
        sys.exit(self.app.exec())

    def get_monitors(self):
        monitors = []
        for config in self.setup.get_setup():
            monitors.append(Monitor(config))
        return monitors

    def get_buttons(self):
        buttons = []
        for monitor in self.monitors:
            buttons.append(Button(monitor))
        return buttons

    def create_labels(self):
        labels = []
        for config in self.setup.get_setup():
            text = self.get_text(config)

            labels.append(QtWidgets.QLabel(
                text,
                alignment = QtCore.Qt.AlignCenter
            ))
        return labels

    def get_text(self, config):
        return "Device: " + config["Device"] + "\nLocation: (" + str(config["x"]) + ", " + str(config["y"]) + ")"


if __name__ == "__main__":
    app = App()
