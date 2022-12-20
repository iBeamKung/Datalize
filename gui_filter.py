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

import altair as alt

import random

import data
import graph
import gui_qt

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

############      Filter Popup

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class filter_gui(QtWidgets.QDialog):
    def __init__(self,name,stringlist=None,stringlist_temp=None,checked=False,icon=None,parent=None,):
        super(filter_gui, self).__init__(parent)
    
        self.name = name
        self.icon = icon
        self.model = QtGui.QStandardItemModel()
        self.listView = QtWidgets.QListView()
        self.resize(360, 300)
    
        for string in stringlist_temp:
            item = QtGui.QStandardItem(string)
            item.setCheckable(True)
            
            if string in stringlist:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            
            self.model.appendRow(item)
    
        self.listView.setModel(self.model)
    
        self.okButton = QtWidgets.QPushButton('OK')
        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.selectButton = QtWidgets.QPushButton('Select All')
        self.unselectButton = QtWidgets.QPushButton('Unselect All')
    
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.okButton)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.selectButton)
        hbox.addWidget(self.unselectButton)
    
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.listView)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
    
        self.setWindowTitle(self.name)
        if self.icon:
            self.setWindowIcon(self.icon)
    
        self.okButton.clicked.connect(self.onAccepted)
        self.cancelButton.clicked.connect(self.reject)
        self.selectButton.clicked.connect(self.select)
        self.unselectButton.clicked.connect(self.unselect)
    
    def onAccepted(self):
        self.choices = [self.model.item(i).text() for i in
                        range(self.model.rowCount())
                        if self.model.item(i).checkState()
                        == QtCore.Qt.Checked]
        self.accept()
    
    def select(self):
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(QtCore.Qt.Checked)
    
    def unselect(self):
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(QtCore.Qt.Unchecked)
            
            
            
            
            
            
class filter_date_gui(QtWidgets.QDialog):
    def __init__(self,name,stringlist=None,stringlist_temp=None,checked=False,icon=None,parent=None,):
        super(filter_date_gui, self).__init__(parent)
    
        self.name = name
        self.icon = icon
        self.model = QtGui.QStandardItemModel()
        self.listView = QtWidgets.QListView()
        self.resize(360, 300)
    
        for string in stringlist_temp:
            item = QtGui.QStandardItem(str(string))
            item.setCheckable(True)
            
            if string in stringlist:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            
            self.model.appendRow(item)
    
        self.listView.setModel(self.model)
    
        self.okButton = QtWidgets.QPushButton('OK')
        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.selectButton = QtWidgets.QPushButton('Select All')
        self.unselectButton = QtWidgets.QPushButton('Unselect All')
    
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.okButton)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.selectButton)
        hbox.addWidget(self.unselectButton)
    
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.listView)
        vbox.addWidget(self.listView)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
    
        self.setWindowTitle(self.name)
        if self.icon:
            self.setWindowIcon(self.icon)
    
        self.okButton.clicked.connect(self.onAccepted)
        self.cancelButton.clicked.connect(self.reject)
        self.selectButton.clicked.connect(self.select)
        self.unselectButton.clicked.connect(self.unselect)
    
    def onAccepted(self):
        self.choices = [int(self.model.item(i).text()) for i in
                        range(self.model.rowCount())
                        if self.model.item(i).checkState()
                        == QtCore.Qt.Checked]
        self.accept()
    
    def select(self):
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(QtCore.Qt.Checked)
    
    def unselect(self):
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(QtCore.Qt.Unchecked)
            
            
            
            
            
            
            
MAXVAL = 650000
class filter_measure_gui(QtWidgets.QDialog):
    
    def __init__(self,in_minValue,in_maxValue,in_minValue_cul,in_maxValue_cul,parent=None):
        super(filter_measure_gui, self).__init__(parent)
        super().__init__()

        self.minValue = in_minValue
        self.maxValue = in_maxValue
        
        self.minValue_cul = in_minValue_cul
        self.maxValue_cul = in_maxValue_cul

        self.sliderMin = MAXVAL
        self.sliderMax = MAXVAL

        self.setupUi(self)
        
    def setupUi(self, Dialog):
        self.sliderMin = MAXVAL
        self.sliderMax = MAXVAL
        
        Dialog.setObjectName("Dialog")
        Dialog.resize(422, 318)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.RangeSelector = QtWidgets.QComboBox(Dialog)
        self.RangeSelector.setObjectName("RangeSelector")
        self.RangeSelector.addItem("Range of values")
        self.RangeSelector.addItem("At least")
        self.RangeSelector.addItem("At most")
        self.RangeSelector.currentTextChanged.connect(self.on_combobox_changed)
        
        self.verticalLayout.addWidget(self.RangeSelector)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        self.slidersFrame = QtWidgets.QFrame(self.groupBox)
        self.slidersFrame.setMaximumSize(QtCore.QSize(16777215, 25))
        self.slidersFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.slidersFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slidersFrame.setObjectName("slidersFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.slidersFrame)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(5, 2, 5, 2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.verticalLayout_3.addWidget(self.slidersFrame)
        """
        self.startSlider = QtWidgets.QSlider(self.slidersFrame)
        self.startSlider.setMaximum(self.sliderMin)
        self.startSlider.setMinimumSize(QtCore.QSize(100, 5))
        self.startSlider.setMaximumSize(QtCore.QSize(16777215, 10))
        
        font = QtGui.QFont()
        font.setKerning(True)
        self.startSlider.setFont(font)
        self.startSlider.setAcceptDrops(False)
        self.startSlider.setAutoFillBackground(False)
        self.startSlider.setOrientation(QtCore.Qt.Horizontal)
        self.startSlider.setInvertedAppearance(True)
        self.startSlider.setObjectName("startSlider")
        self.startSlider.setValue(MAXVAL)
        self.startSlider.sliderReleased.connect(self.startSliderHandler)
        self.horizontalLayout.addWidget(self.startSlider)
        
        self.endSlider = QtWidgets.QSlider(self.slidersFrame)
        self.endSlider.setMaximum(MAXVAL)
        self.endSlider.setMinimumSize(QtCore.QSize(100, 5))
        self.endSlider.setMaximumSize(QtCore.QSize(16777215, 10))
        self.endSlider.setTracking(True)
        self.endSlider.setOrientation(QtCore.Qt.Horizontal)
        self.endSlider.setObjectName("endSlider")
        self.endSlider.setValue(self.sliderMax)
        self.endSlider.sliderReleased.connect(self.endSliderHandler)
        self.horizontalLayout.addWidget(self.endSlider)
        """
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout_min = QtWidgets.QFormLayout()
        self.formLayout_min.setObjectName("formLayout_min")
        self.label_min = QtWidgets.QLabel(self.groupBox)
        self.label_min.setObjectName("label_min")
        self.formLayout_min.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_min)
        self.entry_min = QtWidgets.QLineEdit(self.groupBox)
        self.entry_min.setObjectName("entry_min")
        self.formLayout_min.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.entry_min)
        self.horizontalLayout.addLayout(self.formLayout_min)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.formLayout_max = QtWidgets.QFormLayout()
        self.formLayout_max.setObjectName("formLayout_max")
        self.label_max = QtWidgets.QLabel(self.groupBox)
        self.label_max.setObjectName("label_max")
        self.formLayout_max.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_max)
        self.entry_max = QtWidgets.QLineEdit(self.groupBox)
        self.entry_max.setObjectName("entry_max")
        self.formLayout_max.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.entry_max)
        self.horizontalLayout.addLayout(self.formLayout_max)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.ApplyButton = QtWidgets.QPushButton(Dialog)
        self.ApplyButton.setObjectName("ApplyButton")
        self.verticalLayout_2.addWidget(self.ApplyButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Range of values"))
        self.label_min.setText(_translate("Dialog", "Min : "+str(self.minValue)))
        self.label_max.setText(_translate("Dialog", "Max: "+str(self.maxValue)))
        self.ApplyButton.setText(_translate("Dialog", "Apply"))
        self.ApplyButton.clicked.connect(self.onAccepted)
        self.entry_min.setText(str(self.minValue_cul))
        self.entry_max.setText(str(self.maxValue_cul))
        
    def startSliderHandler(self):
        self.sliderMin = self.startSlider.value()

        #self.minRangeTime = int(self.middleTime - self.halfTimeInterval * self.sliderMin / MAXVAL)
        #print("\n\nNew Min Time Range : ", self.minRangeTime, " Min : ",  self.minTime, "Minddle : ", self.middleTime)

    def endSliderHandler(self):
        self.sliderMax = self.endSlider.value()

        #self.maxRangeTime = int(self.middleTime + self.halfTimeInterval * self.sliderMax / MAXVAL)
        self.maxRangeVal = int((650000/2) + ((650000/2) - (-50000)) * self.sliderMax / 650000)
        print(self.sliderMax)
        
    def onAccepted(self):
        try:
            self.values = [int(self.entry_min.text()),int(self.entry_max.text())]
        except ValueError:
            self.values = [float(self.entry_min.text()),float(self.entry_max.text())]
        self.accept()
        
    def on_combobox_changed(self, value):
        print("combobox changed >>", value)
        if value == "Range of values":
            print("Range of values")
            self.entry_min.setEnabled(True)
            self.entry_max.setEnabled(True)
            #self.entry_min.setText("0")
            #self.entry_max.setText("5")
        if value == "At least":
            print("At least")
            self.entry_min.setEnabled(True)
            self.entry_max.setEnabled(False)
            #self.entry_min.setText("5")
            self.entry_max.setText(str(self.maxValue))
        if value == "At most":
            print("At most")
            self.entry_min.setEnabled(False)
            self.entry_max.setEnabled(True)
            self.entry_min.setText(str(self.minValue))
            #self.entry_max.setText("5")
            
            
            
            
class change_measure_gui(QtWidgets.QDialog):
    def __init__(self,parent=None,):
        super(change_measure_gui, self).__init__(parent)
    
        self.setWindowTitle("Measure")
        self.listView = QtWidgets.QListWidget()
        self.label = QLabel('Select Measure :', self)
        self.resize(360, 300)
    
        self.listView.addItem('Sum')
        self.listView.addItem('Average')
        self.listView.addItem('Median')
        self.listView.addItem('Count')
        self.listView.addItem('Min')
        self.listView.addItem('Max')
        #self.listView.setModel(self.model)
    
        self.okButton = QtWidgets.QPushButton('OK')
        self.cancelButton = QtWidgets.QPushButton('Cancel')
    
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.okButton)
        hbox.addWidget(self.cancelButton)
    
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.label)
        vbox.addWidget(self.listView)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
    
        self.okButton.clicked.connect(self.onAccepted)
        self.cancelButton.clicked.connect(self.reject)
    
    def onAccepted(self):
        self.choices = self.listView.selectedItems()[0].text()
        self.accept()