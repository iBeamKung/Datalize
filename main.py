from importlib.resources import path
from re import S
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
import pandas as pd
import numpy as np
import sys
from io import StringIO
import matplotlib as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

import random

import data
import gui_qt

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Datalize = QtWidgets.QMainWindow()
    ui = gui_qt.Ui_Datalize()
    ui.setupUi(Datalize)
    Datalize.show()
    sys.exit(app.exec_())