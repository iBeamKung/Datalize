from calendar import month
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
import gui_filter

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

############      View Graph

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page().profile().downloadRequested.connect(self.onDownloadRequested)
        self.windows = []
        self.setGeometry(10, 120, 1260, 701)

    @QtCore.pyqtSlot(QtWebEngineWidgets.QWebEngineDownloadItem)
    def onDownloadRequested(self, download):
        if (
            download.state()
            == QtWebEngineWidgets.QWebEngineDownloadItem.DownloadRequested
        ):
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, self.tr("Save as"), download.path()
            )
            if path:
                download.setPath(path)
                download.accept()

    def createWindow(self, type_):
        if type_ == QtWebEngineWidgets.QWebEnginePage.WebBrowserTab:
            window = QtWidgets.QMainWindow(self)
            view = QtWebEngineWidgets.QWebEngineView(window)
            window.resize(640, 480)
            window.setCentralWidget(view)
            window.show()
            return view

    def updateChart(self, chart, **kwargs):
        output = StringIO()
        chart.save(output, "html", **kwargs)
        self.setHtml(output.getvalue())
        #print(output.getvalue())


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

############      Data Table

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= QtCore.Qt.ItemIsEditable
        flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        flags |= QtCore.Qt.ItemIsDragEnabled
        flags |= QtCore.Qt.ItemIsDropEnabled
        return flags

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        try:
            self.layoutAboutToBeChanged.emit()
            self._data = self._data.sort_values(self._data.columns[Ncol], ascending=order)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)

    def printData(self):
        return self._data




"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

############      List Widget

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class ListWidget(QtWidgets.QListWidget):
    def mimeData(self, items):
        md = super().mimeData(items)
        text = "".join([it.text() for it in items])
        md.setText(text)
        return md

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu):
            menu = QtWidgets.QMenu()
            add_drill = menu.addAction('Add Drill')
            delete_list = menu.addAction('Delete')
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if action == add_drill:
                item = source.selectedItems()
                all_item = ""
                for i in item:
                    all_item = all_item + "+" + i.text()
                all_item = all_item[1:]
                print(all_item)
                source.addItem(all_item)
                print(item)
            elif action == delete_list:
                source.takeItem(source.currentRow())
            return True
        return super(ListWidget, self).eventFilter(source, event)

    def dropEvent(self, event):
        super(ListWidget, self).dropEvent(event)

    def updateMeasures(self,measure_in):
        self.measurelist = measure_in

    def updateDimension(self,dimension_in):
        self.dimensionlist = dimension_in

    def iterAllItems(self):
        for i in range(self.count()):
            yield self.item(i)

    def getAllitem_str(self):
        items = []
        for index in range(self.count()):
            if self.item(index).text() != "":
                items.append(self.item(index).text())
        return items

class ListWidgetLine(QtWidgets.QListWidget):
    def __init__(self, parent):
        super(ListWidgetLine, self).__init__(parent)
        self.setViewMode(QListView.IconMode)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.measurelist = {}
        self.datetimelist = {}

    def mimeData(self, items):
        md = super().mimeData(items)
        text = "".join([it.text() for it in items])
        md.setText(text)
        return md

    def dropEvent(self, event):
        event.setDropAction(QtCore.Qt.MoveAction)
        print(event.mimeData().text())
        print(self.measurelist)
        if event.mimeData().text() in self.measurelist:
            self.addItem(self.measurelist[event.mimeData().text()]+"( "+event.mimeData().text()+" )")
        elif event.mimeData().text() in self.datetimelist:
            self.addItem(self.datetimelist[event.mimeData().text()]+"( "+event.mimeData().text()+" )")
        else:
            self.addItem(event.mimeData().text())
        print(self.getAllitem_str())

    def dragLeaveEvent(self, e: QtGui.QDragLeaveEvent) -> None:
        self.takeItem(self.currentRow())

    def contextMenuEvent(self, event):
        print(self.currentRow())
        if self.currentItem().text()[0:5] == "YEAR(":
            self.insertItem(self.currentRow()+1,"QUARTER( "+ self.currentItem().text()[6:-2] + " )")
        elif self.currentItem().text()[0:8] == "QUARTER(":
            self.insertItem(self.currentRow()+1,"MONTH( "+ self.currentItem().text()[9:-2] + " )")
        elif self.currentItem().text()[0:6] == "MONTH(":
            self.insertItem(self.currentRow()+1,"DAY( "+ self.currentItem().text()[7:-2] + " )")
        else:
            if len(self.currentItem().text().split("+")) > 1:
                print("Have DrillDown")
                if (event.type() == QtCore.QEvent.ContextMenu):
                    menu = QtWidgets.QMenu()
                    for i in self.currentItem().text().split("+")[1:]:
                        menu.addAction(i)
                    action = menu.exec_(event.globalPos())
                    if action:
                        item = self.itemAt(event.pos())
                        self.addItem(action.text())
                        print(action.text())
            else:
                print("No DrillDown")

    def iterAllItems(self):
        for i in range(self.count()):
            yield self.item(i)

    def getAllitem_str(self):
        items = []
        for index in range(self.count()):
            if self.item(index).text() != "":
                items.append(self.item(index).text())
        return items

    def updateMeasures(self,measure_in):
        self.measurelist = measure_in

    def updateDatetimes(self,datetime_in):
        self.datetimelist = datetime_in

class MyLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent):
        super(MyLineEdit, self).__init__(parent)
        self.setAcceptDrops( True )

    def dragEnterEvent(self, event):
        if event.mimeData():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData():
            if self.text() != "":
                item_text = self.text() + "," + event.mimeData().text()
            else:
                item_text = event.mimeData().text()
            self.setText(item_text)






"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

############      Main GUI Pyqt5

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Ui_Datalize(object):
    def setupUi(self, Datalize):

        self.df = data.dataSource()
        self.metadata = data.meta_json()

        Datalize.setObjectName("Datalize")
        Datalize.resize(1600, 900)
        Datalize.setMinimumSize(QtCore.QSize(1600, 900))
        self.centralwidget = QtWidgets.QWidget(Datalize)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(296, 19, 1291, 861))
        self.tabWidget.setObjectName("tabWidget")

        """
        ############      Tab DataSource
        """
        self.tab_dataSource = QtWidgets.QWidget()
        self.tab_dataSource.setObjectName("tab_dataSource")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_dataSource)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableView_dataSource = QtWidgets.QTableView(self.tab_dataSource)
        self.tableView_dataSource.setObjectName("tableView_dataSource")
        self.gridLayout_3.addWidget(self.tableView_dataSource, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_dataSource, "")
        """
        ################################################################################
        """

        """
        ############      Tab Graph
        """
        self.tab_graph = QtWidgets.QWidget()
        self.tab_graph.setObjectName("tab_graph")
        self.Layout_verti_colrow_graph = QtWidgets.QWidget(self.tab_graph)
        self.Layout_verti_colrow_graph.setGeometry(QtCore.QRect(10, 40, 1260, 70))
        self.Layout_verti_colrow_graph.setObjectName("Layout_verti_colrow_graph")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.Layout_verti_colrow_graph)
        self.verticalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.Layout_col_graph = QtWidgets.QFormLayout()
        self.Layout_col_graph.setObjectName("Layout_col_graph")
        self.label_columns_graph = QtWidgets.QLabel(self.Layout_verti_colrow_graph)
        self.label_columns_graph.setObjectName("label_columns_graph")
        self.Layout_col_graph.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_columns_graph)

        self.list_col_graph = ListWidgetLine(self.Layout_verti_colrow_graph)
        self.list_col_graph.setMinimumSize(QtCore.QSize(1203, 29))
        self.list_col_graph.setMaximumSize(QtCore.QSize(1203, 29))
        self.list_col_graph.setObjectName("list_col_graph")

        self.Layout_col_graph.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.list_col_graph)
        self.verticalLayout_6.addLayout(self.Layout_col_graph)
        self.Layout_row_graph = QtWidgets.QFormLayout()
        self.Layout_row_graph.setSpacing(0)
        self.Layout_row_graph.setObjectName("Layout_row_graph")
        self.label_row_graph = QtWidgets.QLabel(self.Layout_verti_colrow_graph)
        self.label_row_graph.setObjectName("label_row_graph")
        self.Layout_row_graph.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_row_graph)

        self.list_row_graph = ListWidgetLine(self.Layout_verti_colrow_graph)
        self.list_row_graph.setMinimumSize(QtCore.QSize(1223, 29))
        self.list_row_graph.setMaximumSize(QtCore.QSize(1223, 29))
        self.list_row_graph.setObjectName("list_row_graph")

        self.Layout_row_graph.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.list_row_graph)
        self.verticalLayout_6.addLayout(self.Layout_row_graph)
        self.label_gruop_graph = QtWidgets.QLabel(self.tab_graph)
        self.label_gruop_graph.setGeometry(QtCore.QRect(10, 10, 44, 16))
        self.label_gruop_graph.setObjectName("label_gruop_graph")
        self.btn_submit_graph = QtWidgets.QPushButton(self.tab_graph)
        self.btn_submit_graph.setGeometry(QtCore.QRect(920, 10, 75, 23))
        self.btn_submit_graph.setObjectName("btn_submit_graph")
        self.comboBox_selector = QtWidgets.QComboBox(self.tab_graph)
        self.comboBox_selector.setGeometry(QtCore.QRect(1010, 10, 261, 22))
        self.comboBox_selector.setObjectName("comboBox_selector")
        self.comboBox_selector.addItem("")
        self.comboBox_selector.addItem("")
        self.comboBox_selector.addItem("")
        self.comboBox_selector.addItem("")

        self.label_angle_graph = QtWidgets.QLabel(self.tab_graph)
        self.label_angle_graph.setGeometry(QtCore.QRect(90, 10, 44, 16))
        self.label_angle_graph.setObjectName("label_gruop_graph_2")
        self.label_color_graph = QtWidgets.QLabel(self.tab_graph)
        self.label_color_graph.setGeometry(QtCore.QRect(510, 10, 44, 16))
        self.label_color_graph.setObjectName("label_gruop_graph_3")

        self.list_angle_graph = ListWidgetLine(self.tab_graph)
        self.list_angle_graph.setGeometry(QtCore.QRect(140, 10, 350, 29))
        self.list_angle_graph.setObjectName("list_angle_graph")

        self.list_color_graph = ListWidgetLine(self.tab_graph)
        self.list_color_graph.setGeometry(QtCore.QRect(560, 10, 350, 29))
        self.list_color_graph.setObjectName("list_color_graph")

        self.label_angle_graph.hide()
        self.label_color_graph.hide()
        self.list_angle_graph.hide()
        self.list_color_graph.hide()

        self.tableView_s1 = QtWidgets.QTableView(self.tab_graph)
        self.tableView_s1.setGeometry(QtCore.QRect(10, 120, 1260, 701))
        self.tableView_s1.setObjectName("tableView_s1")
        #self.tableView_s1.show()

        self.view_graph = WebEngineView(parent = self.tab_graph)
        self.view_graph.hide()

        self.tabWidget.addTab(self.tab_graph, "")
        """
        ################################################################################
        """

        """
        ############      Group File Manager
        """
        self.group_filemanager = QtWidgets.QGroupBox(self.centralwidget)
        self.group_filemanager.setEnabled(True)
        self.group_filemanager.setGeometry(QtCore.QRect(11, 11, 261, 141))
        self.group_filemanager.setMinimumSize(QtCore.QSize(0, 0))
        self.group_filemanager.setMaximumSize(QtCore.QSize(16777215, 425))
        self.group_filemanager.setObjectName("group_filemanager")
        self.gridLayout = QtWidgets.QGridLayout(self.group_filemanager)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.Layout_verti = QtWidgets.QVBoxLayout()
        self.Layout_verti.setSpacing(10)
        self.Layout_verti.setObjectName("Layout_verti")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_file_Filepath = QtWidgets.QLabel(self.group_filemanager)
        self.label_file_Filepath.setObjectName("label_file_Filepath")
        self.verticalLayout.addWidget(self.label_file_Filepath)
        self.label_file_col_stat = QtWidgets.QLabel(self.group_filemanager)
        self.label_file_col_stat.setObjectName("label_file_col_stat")
        self.verticalLayout.addWidget(self.label_file_col_stat)
        self.label_file_row_stat = QtWidgets.QLabel(self.group_filemanager)
        self.label_file_row_stat.setObjectName("label_file_row_stat")
        self.verticalLayout.addWidget(self.label_file_row_stat)
        self.verticalLayout.setStretch(1, 5)
        self.Layout_verti.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_file_add = QtWidgets.QPushButton(self.group_filemanager)
        self.btn_file_add.setObjectName("btn_file_add")
        self.horizontalLayout.addWidget(self.btn_file_add)
        self.btn_file_import = QtWidgets.QPushButton(self.group_filemanager)
        self.btn_file_import.setObjectName("btn_file_import")
        self.horizontalLayout.addWidget(self.btn_file_import)
        self.btn_file_export = QtWidgets.QPushButton(self.group_filemanager)
        self.btn_file_export.setEnabled(False)
        self.btn_file_export.setObjectName("btn_file_export")
        self.horizontalLayout.addWidget(self.btn_file_export)
        self.Layout_verti.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.Layout_verti, 0, 0, 1, 1)
        """
        ################################################################################
        """

        """
        ############      List Dimensions & Measures
        """
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 160, 261, 711))
        self.widget.setObjectName("widget")

        self.Layout_diamea = QtWidgets.QVBoxLayout(self.widget)
        self.Layout_diamea.setContentsMargins(0, 0, 0, 0)
        self.Layout_diamea.setSpacing(5)
        self.Layout_diamea.setObjectName("Layout_diamea")

        self.label_diamea = QLabel('Dimension :')
        self.list_dimensions = ListWidget(self.widget)
        self.list_dimensions.setDragEnabled(True)
        self.list_dimensions.setAcceptDrops(True)
        self.list_dimensions.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_dimensions.installEventFilter(self.list_dimensions)
        self.list_dimensions.setDefaultDropAction(Qt.MoveAction)
        self.list_dimensions.setObjectName("list_dimensions")

        self.Layout_diamea.addWidget(self.label_diamea)
        self.Layout_diamea.addWidget(self.list_dimensions)

        self.label_datetime = QLabel('Datetime :')
        self.list_datetime = ListWidget(self.widget)
        self.list_datetime.setDragEnabled(True)
        self.list_datetime.setObjectName("list_dimensions")

        self.Layout_diamea.addWidget(self.label_datetime)
        self.Layout_diamea.addWidget(self.list_datetime)

        self.label_measures = QLabel('Measure :')
        self.list_measures = ListWidget(self.widget)
        self.list_measures.setDragEnabled(True)
        self.list_measures.setAcceptDrops(True)
        self.list_measures.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_measures.setDefaultDropAction(Qt.MoveAction)
        self.list_measures.setObjectName("list_measures")

        self.btn_savelist = QtWidgets.QPushButton('Save')
        self.btn_savelist.clicked.connect(self.SaveDimensionAndMeasure)

        self.Layout_diamea.addWidget(self.label_measures)
        self.Layout_diamea.addWidget(self.list_measures)
        self.Layout_diamea.addWidget(self.btn_savelist)
        """
        ################################################################################
        """

        Datalize.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Datalize)
        self.statusbar.setObjectName("statusbar")
        Datalize.setStatusBar(self.statusbar)

        self.retranslateUi(Datalize)
        #self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Datalize)

    def retranslateUi(self, Datalize):
        _translate = QtCore.QCoreApplication.translate
        Datalize.setWindowTitle(_translate("Datalize", "Datalize"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_dataSource), _translate("Datalize", "DataSource"))

        self.label_color_graph.setText(_translate("Datalize", "Color :"))
        self.label_angle_graph.setText(_translate("Datalize", "Angle :"))
        self.label_columns_graph.setText(_translate("Datalize", "Dimensions :"))
        self.label_row_graph.setText(_translate("Datalize", "Measures :"))
        self.label_gruop_graph.setText(_translate("Datalize", "Group by"))
        self.comboBox_selector.setItemText(0, _translate("Datalize", "Grid Table"))
        self.comboBox_selector.setItemText(1, _translate("Datalize", "Bar Chart"))
        self.comboBox_selector.setItemText(2, _translate("Datalize", "Pie Chart"))
        self.comboBox_selector.setItemText(3, _translate("Datalize", "Line Chart"))
        self.btn_submit_graph.setText(_translate("Datalize", "Submit"))
        self.btn_submit_graph.clicked.connect(self.btn_submit_graph_clk)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_graph), _translate("Datalize", "Graph"))

        self.group_filemanager.setTitle(_translate("Datalize", "File Data"))
        self.label_file_Filepath.setText(_translate("Datalize", "File : "))
        self.label_file_col_stat.setText(_translate("Datalize", "Columns : "))
        self.label_file_row_stat.setText(_translate("Datalize", "Rows : "))
        self.btn_file_add.setText(_translate("Datalize", "Add"))
        self.btn_file_import.setText(_translate("Datalize", "Import"))
        self.btn_file_export.setText(_translate("Datalize", "export"))
        self.btn_file_add.clicked.connect(self.btn_file_add_clk)
        self.btn_file_import.clicked.connect(self.btn_file_import_clk)
        #self.btn_file_export.clicked.connect(self.btn_file_export_clk)

        self.list_dimensions.itemDoubleClicked.connect(self.FilterDimensionsClicked)
        self.list_datetime.itemDoubleClicked.connect(self.FilterDatetimeClicked)
        self.list_measures.itemDoubleClicked.connect(self.FilterMeasuresClicked)

        self.list_col_graph.itemDoubleClicked.connect(self.MeasuresClicked)
        self.list_row_graph.itemDoubleClicked.connect(self.MeasuresClicked)

        self.comboBox_selector.currentTextChanged.connect(self.on_combobox_changed)

    def on_combobox_changed(self, value):

        print("combobox changed >>", value)
        if value == "Grid Table":
            self.view_graph.hide()
            self.tableView_s1.show()
            self.label_columns_graph.setText("Dimensions :")
            self.label_row_graph.setText("Measures :")
        else:
            self.label_columns_graph.setText("Columns :")
            self.label_row_graph.setText("Row :")
            self.view_graph.show()
            self.tableView_s1.hide()

        if value == "Pie Chart":
            self.label_angle_graph.show()
            self.label_color_graph.show()
            self.list_angle_graph.show()
            self.list_color_graph.show()
        else:
            self.label_angle_graph.hide()
            self.label_color_graph.hide()
            self.list_angle_graph.hide()
            self.list_color_graph.hide()

    def SaveDimensionAndMeasure(self):
        self.metadata.save(self.list_col_graph.getAllitem_str(),self.list_row_graph.getAllitem_str(),self.list_dimensions.getAllitem_str(),self.list_datetime.getAllitem_str(),self.list_measures.getAllitem_str())

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    ############      Button Fuction

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    def btn_file_add_clk(self):

        file , check = QFileDialog.getOpenFileName(None, "Select Datafile","", "CSV Files (*.csv);;CSV Files,Excel (*.csv,*.xlsx)")
        if check:
            self.df.addData(file)
            
            self.label_file_Filepath.setText("File : "+ file)
            self.label_file_col_stat.setText("Columns : "+ str(self.df.colDisplay()))
            self.label_file_row_stat.setText("Rows : "+ str(self.df.rowDisplay()))

            self.btn_file_export.setEnabled(False)

            dataModel = pandasModel(self.df.printDataOG())
            self.tableView_dataSource.reset()
            self.tableView_dataSource.setModel(dataModel)
            self.tableView_dataSource.setSortingEnabled(True)
            self.btn_file_add.setEnabled(True)

            self.list_dimensions.clear()
            self.list_datetime.clear()
            self.list_measures.clear()
            
            dataHeader = data.dataHandler(self.df.printDataOG())
            filter_header = ['id', 'code']
            head_obj = dataHeader.selectedHeaderstr()
            all = []
            measureslist = {}
            datetimelist = {}

            for i in sorted(dataHeader.selectedHeadernum()):
                x = i.lower().split()
                matching = [s for s in x if any(xs in s for xs in filter_header)]
                if matching:
                    head_obj.append(i)
                else:
                    all.append(i)
                    measureslist[i] = "SUM"

            for i in sorted(head_obj):
                self.list_dimensions.addItem(i)

            for i in sorted(dataHeader.selectedHeaderdate()):
                self.list_datetime.addItem(i)
                datetimelist[i] = "YEAR"

            for i in all:
                self.list_measures.addItem(i)

            self.list_col_graph.updateMeasures(measureslist)
            self.list_row_graph.updateMeasures(measureslist)
            self.list_col_graph.updateDatetimes(datetimelist)
            self.list_row_graph.updateDatetimes(datetimelist)

    def btn_file_import_clk(self):
        file , check = QFileDialog.getOpenFileName(None, "Select Datafile","", "CSV Files (*.csv);;Excel (*.xlsx)")
        if check:
            self.df.importData(file)

            self.label_file_Filepath.setText("File : "+ file)
            self.label_file_col_stat.setText("Columns : "+ str(self.df.colDisplay()))
            self.label_file_row_stat.setText("Rows : "+ str(self.df.rowDisplay()))

            self.btn_file_export.setEnabled(False)

            dataModel = pandasModel(self.df.printDataOG())
            self.tableView_dataSource.reset()
            self.tableView_dataSource.setModel(dataModel)
            self.tableView_dataSource.setSortingEnabled(True)
            self.btn_file_add.setEnabled(True)

            self.list_dimensions.clear()
            self.list_datetime.clear()
            self.list_measures.clear()

            print("load json meta")
            meta = self.metadata.load(file)
            if meta:
                print("have metadata!")
                measureslist = {}
                datetimelist = {}
                dataHeader = data.dataHandler(self.df.printDataOG())
                filter_header = ['id', 'code']
                head_obj = dataHeader.selectedHeaderstr()
                for i in sorted(dataHeader.selectedHeadernum()):
                    x = i.lower().split()
                    matching = [s for s in x if any(xs in s for xs in filter_header)]
                    if matching:
                        head_obj.append(i)
                    else:
                        measureslist[i] = "SUM"
                for i in sorted(dataHeader.selectedHeaderdate()):
                    datetimelist[i] = "YEAR"

                self.list_col_graph.updateMeasures(measureslist)
                self.list_row_graph.updateMeasures(measureslist)
                self.list_col_graph.updateDatetimes(datetimelist)
                self.list_row_graph.updateDatetimes(datetimelist)

                """ Add list to listwidget """
                for i in meta[0]:
                    self.list_col_graph.addItem(i)
                for i in meta[1]:
                    self.list_row_graph.addItem(i)
                for i in meta[2]:
                    self.list_dimensions.addItem(i)
                for i in meta[3]:
                    self.list_datetime.addItem(i)
                for i in meta[4]:
                    self.list_measures.addItem(i)
                """"""""""""""""""""""""""""""

            else:
                print("no data in metadata!!")
                dataHeader = data.dataHandler(self.df.printDataOG())
                filter_header = ['id', 'code']
                head_obj = dataHeader.selectedHeaderstr()
                all = []
                measureslist = {}
                datetimelist = {}

                for i in sorted(dataHeader.selectedHeadernum()):
                    x = i.lower().split()
                    matching = [s for s in x if any(xs in s for xs in filter_header)]
                    if matching:
                        head_obj.append(i)
                    else:
                        all.append(i)
                        measureslist[i] = "SUM"

                for i in sorted(head_obj):
                    self.list_dimensions.addItem(i)

                for i in sorted(self.df.selectedHeaderdate()):
                    self.list_datetime.addItem(i)
                    datetimelist[i] = "YEAR"

                for i in all:
                    self.list_measures.addItem(i)

                self.list_col_graph.updateMeasures(measureslist)
                self.list_row_graph.updateMeasures(measureslist)
                self.list_col_graph.updateDatetimes(datetimelist)
                self.list_row_graph.updateDatetimes(datetimelist)

    def btn_submit_graph_clk(self):
        print("Submit Graph")

        graph_select = str(self.comboBox_selector.currentText())

        print(graph_select)
        if graph_select == "Grid Table":
            row = self.list_row_graph.getAllitem_str()
            for count,i in enumerate(row):
                if len(i.split("+")) > 1:
                    row[count]=i.split("+")[0]
            col = self.list_col_graph.getAllitem_str()
            for count,i in enumerate(col):
                if len(i.split("+")) > 1:
                    col[count]=i.split("+")[0]
            all = self.list_row_graph.getAllitem_str()
            if col != [""]:
                all.extend(col)

            print(row,":",col,":",all)

            dataEdit = data.dataHandler(self.df.printData()).group(col,row)
            self.tableView_s1.reset()
            dataModel = pandasModel(dataEdit)
            self.tableView_s1.setModel(dataModel)

        elif graph_select == "Bar Chart":
            row = self.list_row_graph.getAllitem_str()
            for count,i in enumerate(row):
                if len(i.split("+")) > 1:
                    row[count]=i.split("+")[0]
            col = self.list_col_graph.getAllitem_str()
            for count,i in enumerate(col):
                if len(i.split("+")) > 1:
                    col[count]=i.split("+")[0]
            chart = graph.draw_graph().BarChart(self.df,col,row)
            self.view_graph.updateChart(chart)

        elif graph_select == "Pie Chart":
            row = self.list_row_graph.getAllitem_str()
            col = self.list_col_graph.getAllitem_str()
            angle = self.list_angle_graph.getAllitem_str()
            color = self.list_color_graph.getAllitem_str()
            chart = graph.draw_graph().PieChart(self.df,col,row,color,angle)
            self.view_graph.updateChart(chart)

        elif graph_select == "Line Chart":
            row = self.list_row_graph.getAllitem_str()
            col = self.list_col_graph.getAllitem_str()
            chart = graph.draw_graph().LineChart(self.df,col,row)
            self.view_graph.updateChart(chart)


    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    ############      Filter GUI Fuction

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    def FilterDimensionsClicked(self, item):
        filter_header = ['date']

        x = item.text().lower().split()
        matching = [s for s in x if any(xs in s for xs in filter_header)]
        if not matching:
            filter_ui = gui_filter.filter_gui('Filters : '+str(item.text()),self.df.printData()[item.text()].drop_duplicates().astype(str).values.tolist(),self.df.printDataTemp()[item.text()].drop_duplicates().astype(str).values.tolist(), checked=True)
            if filter_ui.exec_() == QtWidgets.QDialog.Accepted:
                print(filter_ui.choices)
                self.df.filtersData(item.text(),filter_ui.choices)

    def FilterMeasuresClicked(self, item):
        filter_ui = gui_filter.filter_measure_gui(self.df.printMinValueOG(item.text()),self.df.printMaxValueOG(item.text()),self.df.printMinValue(item.text()),self.df.printMaxValue(item.text()))
        if filter_ui.exec_() == QtWidgets.QDialog.Accepted:
                print(filter_ui.values)
                self.df.filtersMeasures(item.text(),filter_ui.values)

    def FilterDatetimeClicked(self, item):
        if item.text()[0:5] == "YEAR(":
            print("SSSSS")
            print(self.df.getYear(item.text()[6:-2]),self.df.yearData[item.text()[6:-2]])
        filter_ui = gui_filter.filter_date_gui('Filters : '+str(item.text()),self.df.getYear(item.text()),self.df.yearData[item.text()], checked=True)
        if filter_ui.exec_() == QtWidgets.QDialog.Accepted:
            print(filter_ui.choices)
            self.df.filtersDate(item.text(),filter_ui.choices)

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    ############      Col,Row GUI Fuction

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    def MeasuresClicked(self, item):
        filter_header = ['SUM(','AVG(','COU(','MED(','MIN(','MAX(']

        x = item.text().split()
        matching = [s for s in x if any(xs in s for xs in filter_header)]
        if matching:
            print("Measure")
            Measures_ui = gui_filter.change_measure_gui()
            if Measures_ui.exec_() == QtWidgets.QDialog.Accepted:
                print(Measures_ui.choices)
                if(Measures_ui.choices == "Sum"):
                    item.setText("SUM"+item.text()[3:])
                elif(Measures_ui.choices == "Average"):
                    item.setText("AVG"+item.text()[3:])
                elif(Measures_ui.choices == "Median"):
                    item.setText("MED"+item.text()[3:])
                elif(Measures_ui.choices == "Count"):
                    item.setText("COU"+item.text()[3:])
                elif(Measures_ui.choices == "Max"):
                    item.setText("MAX"+item.text()[3:])
                elif(Measures_ui.choices == "Min"):
                    item.setText("MIN"+item.text()[3:])

if __name__ == "__main__":
    import sys
    #metadata = data.meta_json()
    app = QtWidgets.QApplication(sys.argv)
    Datalize = QtWidgets.QMainWindow()
    ui = Ui_Datalize()
    ui.setupUi(Datalize)
    Datalize.show()
    sys.exit(app.exec_())