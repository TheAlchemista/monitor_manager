import sys
import os
from PySide6 import QtCore, QtWidgets, QtGui


class Button:
    def __init__(self, monitor):
        self.button = QtWidgets.QPushButton("Turn monitor off")
        self.monitor = monitor
        # Add methods
        self.button.clicked.connect(self.on_click)
        self.choose_icon()

    def choose_icon(self):
        if self.monitor.config["x"] == 0 and self.monitor.config["y"] == 0:
            pass
        else:
            if abs(self.monitor.config["x"]) > abs(self.monitor.config["y"]):
                if self.monitor.config["x"] > 0:
                    self.button.setIcon(QtGui.QIcon("./icons/arrow_right.png"))
                elif self.monitor.config["x"] < 0:
                    self.button.setIcon(QtGui.QIcon("./icons/arrow_left.png"))
            else:
                if self.monitor.config["y"] < 0:
                    self.button.setIcon(QtGui.QIcon("./icons/arrow_up.png"))
                elif self.monitor.config["y"] > 0:
                    self.button.setIcon(QtGui.QIcon("./icons/arrow_down.png"))

    @QtCore.Slot()
    def on_click(self):
        if self.monitor.config["State"] == 'on':
            self.turn_monitor_off()
        else:
            self.turn_monitor_on()

    def turn_monitor_off(self):
        os.system("dccmd -monitor=" + self.monitor.config["Device"] + " -detach")
        self.monitor.set_turned_off()
        self.button.setText("Turn monitor on")
        print("Succesfully turned monitor off.")

    def turn_monitor_on(self):
        os.system("dccmd -monitor=" +
            self.monitor.config["Device"] +
            " -width=max -height=max" +
            " -lx=" + str(self.monitor.config["x"]) +
            " -ty=" + str(self.monitor.config["y"]))
        self.monitor.set_turned_on()
        self.button.setText("Turn monitor off")
        print("Succesfully turned monitor on.")

    def get_button(self):
        return self.button


class Exit_Button(QtWidgets.QPushButton):
    def __init__(self):
        super().__init__(text="Exit")
        self.clicked.connect(self.on_click)

    @QtCore.Slot()
    def on_click(self):
        sys.exit(0)
