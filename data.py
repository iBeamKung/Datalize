from importlib.resources import path
from re import S
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
import pandas as pd
import copy
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

import datetime as dt
import datetime
import random
import io
import json
import os
import hashlib

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

############      Data

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class dataSource():
    def __init__(self):
        self.data = pd.DataFrame()
        self.data_temp = pd.DataFrame()
        self.data_OG = pd.DataFrame()
        self.data_Datetime = pd.DataFrame()
        self.yearData = {}
        self.fillerData = {}
        self.dimensions = []
        self.measures = []
        self.timedate = []
        self.maxValue_OG = {}
        self.minValue_OG = {}
    
    def printDataTemp(self):
        return self.data_temp
    
    def printDataOG(self):
        return self.data_OG
    
    def printData(self):
        return self.data
    
    def printDimensions(self):
        return self.dimensions
    
    def printDatetime(self):
        return self.timedate
    
    def printMeasures(self):
        return self.measures
    
    def printMaxValue(self,header):
        return self.data[header].max()
    
    def printMinValue(self,header):
        return self.data[header].min()
    
    def printMaxValueOG(self,header):
        return self.maxValue_OG[header]
    
    def printMinValueOG(self,header):
        return self.minValue_OG[header]
    
    def selectedHeaderstr(self):
        return self.data_OG.select_dtypes(['object','string']).columns.values.tolist()
    
    def selectedHeaderdate(self):
        return self.data_OG.select_dtypes(['datetime']).columns.values.tolist()
    
    def selectedHeadernum(self):
        return self.data_OG.select_dtypes(['int64','float64']).columns.values.tolist()
    
    def rowDisplay(self):
        return self.data.shape[0]
    
    def colDisplay(self):
        return self.data_OG.shape[1]
    
    def importData(self,pathData):
        print(pathData)
        if pathData[-5:].lower() == ".xlsx":
            print(pathData[-5:].lower())
            self.data = pd.read_excel(pathData)
            print(pathData[-5:].lower())

        elif pathData[-4:].lower() == ".csv":
            encodings = ["utf-8", "cp1252"]
            for encoding in encodings:
                try:
                    self.data = pd.read_csv(pathData, encoding=encoding)
                    #print(encoding)
                except ValueError:
                    continue

        self.data_temp = self.data
        self.data_OG = copy.copy(self.data)
        self.filterData = dict.fromkeys(self.data.columns.values.tolist())

        filter_header = ['date']
        list_head = self.data.columns.values.tolist()
        
        for i in list_head:
            x = i.lower().split()
            matching = [s for s in x if any(xs in s for xs in filter_header)]
            if matching:
                #self.data[i] = pd.to_datetime(self.data[i], format='%d/%m/%Y')
                print(i)
                self.data_OG[i] = pd.to_datetime(self.data_OG[i],dayfirst=True)
                
                print(self.data_OG[i])
                self.yearData[i] = sorted(self.data_OG[i].dt.year.drop_duplicates().to_list())
                #self.data[i] = self.data[i].dt.strftime('%d/%m/%Y')

        for i in list_head:
            x = i.lower().split()
            matching = [s for s in x if any(xs in s for xs in filter_header)]
            if matching:
                #self.data[i] = pd.to_datetime(self.data[i], format='%d/%m/%Y')
                print(i)
                self.data[i] = pd.to_datetime(self.data[i],dayfirst=True)
                self.data[i + ' : Day'] = pd.DatetimeIndex(self.data[i]).day
                self.data[i + ' : Month'] = pd.DatetimeIndex(self.data[i]).month
                self.data[i + ' : Quarter'] = pd.DatetimeIndex(self.data[i]).quarter
                self.data[i + ' : Year'] = pd.DatetimeIndex(self.data[i]).year
                
                print(self.data[i])
                self.yearData[i] = sorted(self.data[i].dt.year.drop_duplicates().to_list())
                #self.data[i] = self.data[i].dt.strftime('%d/%m/%Y')

        filter_header = ['id', 'code', 'year']
        list_head = self.data_OG.columns.values.tolist()
        for i in list_head:
            x = i.lower().split()
            matching = [s for s in x if any(xs in s for xs in filter_header)]
            if matching:
                self.data[i] = self.data[i].astype('string')
                self.data_OG[i] = self.data_OG[i].astype('string')
        """
        list_head = self.data.columns.values.tolist()

        for i in list_head:
            if self.data.dtypes[i] == np.float64 or self.data.dtypes[i] == np.int64:
                self.measures.append(i)
                self.minValue_OG[i] = self.data[i].min()
                self.maxValue_OG[i] = self.data[i].max()
            elif self.data.dtypes[i]== "string" or self.data.dtypes[i]=="object":
                self.dimensions.append(i)
            else:
                self.timedate.append(i)
        """
        list_head = self.data_OG.columns.values.tolist()
        for i in list_head:
            if self.data_OG.dtypes[i] == np.float64 or self.data_OG.dtypes[i] == np.int64:
                self.measures.append(i)
                self.minValue_OG[i] = self.data_OG[i].min()
                self.maxValue_OG[i] = self.data_OG[i].max()
            elif self.data_OG.dtypes[i]== "string" or self.data_OG.dtypes[i]=="object":
                self.dimensions.append(i)
            else:
                self.timedate.append(i)
        #print("Import Data Success!")

    def getYear(self,head):
        return sorted(self.data[head].dt.year.drop_duplicates().to_list())

    def addData(self,pathData):
        if pathData[-5:].lower() == ".xlsx":
            print(pathData[-5:].lower())
            add_data = pd.read_excel(pathData)
            print(pathData[-5:].lower())

        elif pathData[-4:].lower() == ".csv":
            encodings = ["utf-8", "cp1252"]
            for encoding in encodings:
                try:
                    add_data = pd.read_csv(pathData, encoding=encoding)
                    #print(encoding)
                except ValueError:
                    continue
                
        add_data = pd.read_csv(pathData,encoding='windows-1254')
        temp_data = self.data_OG
        self.data_OG = pd.concat([temp_data,add_data], ignore_index=True)
        
        self.data = self.data_OG
        
        filter_header = ['date']
        list_head = self.data_OG.columns.values.tolist()
        
        for i in list_head:
            x = i.lower().split()
            matching = [s for s in x if any(xs in s for xs in filter_header)]
            if matching:
                #self.data[i] = pd.to_datetime(self.data[i], format='%d/%m/%Y')
                print(i)
                self.data[i] = pd.to_datetime(self.data[i],dayfirst=True)
                self.data[i + ' : Day'] = pd.DatetimeIndex(self.data[i]).day
                self.data[i + ' : Month'] = pd.DatetimeIndex(self.data[i]).month
                self.data[i + ' : Quarter'] = pd.DatetimeIndex(self.data[i]).quarter
                self.data[i + ' : Year'] = pd.DatetimeIndex(self.data[i]).year
                
                print(self.data[i])
                self.yearData[i] = sorted(self.data[i].dt.year.drop_duplicates().to_list())
        
        print(self.data)

    def filtersData(self,head,filter):
        self.filterData[head] = filter
        self.data = self.data_temp
        data_filter = self.data
        for key, value in self.filterData.items():
            if value != None:
                print("Filter =>",key,value)
                self.data = self.data.loc[data_filter[key].isin(value)]
        print("Filter")
        return True
    
    def filtersMeasures(self,head,values):
        self.filterData[head] = filter
        self.data = self.data_temp
        self.data = self.data[(self.data[head] >= values[0]) & (self.data[head] <= values[1])]
        print("Filter : Measure")
        return self.data
    
    def filtersDate(self,head,filter):
        self.filterData[head] = filter
        self.data = self.data_temp
        data_filter = self.data
        for key, value in self.filterData.items():
            if value != None:
                print("Filter =>",key,value)
                self.data = self.data[data_filter[key].dt.year.isin(filter)]
        print("Filter : Date")
        return True


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

############      Manage Data

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class dataHandler():
    def __init__(self, data):
        self._data = data

    def rowCount(self):
        return self._data.shape[0]

    def columnCount(self):
        return self._data.shape[1]

    def sortData(self,col):
        self._data.sort_values(by=col, inplace=True)

    def columnSelect(self,selector):
        return self._data[selector]

    def dataExport(self):
        return self._data

    def group(self,dimension,measure):

        print(dimension,len(dimension),measure,len(measure))
        if dimension == [""]:
            dimension = []
        if measure == [""]:
            measure = []
        
        col_add = []
        measure_agg = {}
        
        for count,i in enumerate(dimension):
            if i[0:5] == "YEAR(":
                dimension[count] = i[6: -2] + " : Year"
            elif i[0:8] == "QUARTER(":
                dimension[count] = i[9: -2] + " : Quarter"
            elif i[0:6] == "MONTH(":
                dimension[count] = i[7: -2] + " : Month"
            elif i[0:4] == "DAY(":
                dimension[count] = i[5: -2] + " : Day"
        
        for i in measure:
    
            if i[5:-2] not in measure_agg:
                measure_agg[i[5:-2]] = []

            if i[0:4] == "SUM(":
                measure_agg[i[5:-2]].append("sum")
                col_add.append(str(i[5:-2]+": SUM"))
            elif i[0:4] == "AVG(":
                measure_agg[i[5:-2]].append("mean")
                col_add.append(str(i[5:-2]+": AVG"))
            elif i[0:4] == "MED(":
                measure_agg[i[5:-2]].append("median")
                col_add.append(str(i[5:-2]+": MED"))
            elif i[0:4] == "COU(":
                measure_agg[i[5:-2]].append("count")
                col_add.append(str(i[5:-2]+": Count"))
            elif i[0:4] == "MAX(":
                measure_agg[i[5:-2]].append("max")
                col_add.append(str(i[5:-2]+": MAX"))
            elif i[0:4] == "MIN(":
                measure_agg[i[5:-2]].append("min")
                col_add.append(str(i[5:-2]+": MIN"))
                
        if len(measure):
            datasum = self._data.groupby(dimension).agg(measure_agg)
            datasum.columns = col_add
        else:
            datasum = self._data.groupby(dimension).mean().iloc[:,:0]
        return datasum.reset_index()
    
    def select(self,by):
        return self._data[by]
    
    def getHeader(self):
        return self._data.columns.values.tolist()
    
    def getYear(self,head):
        return sorted(self._data[head].dt.year.drop_duplicates().to_list())
    
    def getType(self):
        return self._data.dtypes
    
    def selectedHeaderstr(self):
        return self._data.select_dtypes(['object','string']).columns.values.tolist()
    
    def selectedHeaderdate(self):
        return self._data.select_dtypes(['datetime']).columns.values.tolist()
    
    def selectedHeadernum(self):
        return self._data.select_dtypes(['int64','float64']).columns.values.tolist()
    
class meta_json():
    def __init__(self):
        if os.path.isfile("meta.json") and os.access("/", os.R_OK):
            # checks if file exists
            print ("File exists and is readable")
            f = open('meta.json')
            self.meta = json.load(f)
        else:
            print ("Either file is missing or is not readable, creating file...")
            with io.open(os.path.join("", 'meta.json'), 'w') as db_file:
                db_file.write(json.dumps(
                                            {
                                                "Datalize":[]
                                            }
                                        ))
            f = open('meta.json')
            self.meta = json.load(f)

    def save(self,col,row,dia,date,mea):
        print("Metadata Save!")
        md5_hash = hashlib.md5()
        a_file = open(self.data_file_path, "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        for i in self.meta['Datalize']:
            #if i["file_path"] == self.data_file_path and i["md5"] == digest:
            if i["md5"] == digest:
                i["col"] = col
                i["row"] = row
                i["dimensions"] = dia
                i["datetime"] = date
                i["measures"] = mea
                with open('meta.json', 'w') as f:
                    json.dump(self.meta, f, indent = 4)
                return True
        self.meta['Datalize'].append(
            {
                "file_path": self.data_file_path,
                "md5": digest,
                "col": col,
                "row": row,
                "dimensions": dia,
                "datetime": date,
                "measures": mea
            }
            )
        with open('meta.json', 'w') as f:
            json.dump(self.meta, f, indent = 4)

    def load(self,in_data_file_path):
        self.data_file_path = in_data_file_path
        md5_hash = hashlib.md5()
        a_file = open(self.data_file_path, "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        for i in self.meta['Datalize']:
            #if i["file_path"] == self.data_file_path and i["md5"] == digest:
            if i["md5"] == digest:
                return [i["col"],i["row"],i["dimensions"],i["datetime"],i["measures"]]
        return False
        
if __name__ == "__main__":
    df = dataSource()
    df.importData("testfile_1.csv")
    print(df.printDimensions())
    print(df.printDatetime())
    print(df.printMeasures())