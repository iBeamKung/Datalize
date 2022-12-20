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


class draw_graph():
    def __init__(self):
        self.data = pd.DataFrame()
        self.data_temp = pd.DataFrame()
        self.data_OG = pd.DataFrame()
        self.fillerData = {}
        self.dimensions = []
        self.measures = []
    
    def BarChart(self,data_in,col_list,row_list):
        print(col_list,":",row_list)
        
        all_list = []
        col_dimensions_list = []
        row_dimensions_list = []
        col_measures_list = []
        row_measures_list = []
        col_dimensions = ''
        row_dimensions = ''
        x_measure,y_measure = '',''
        x_agg,y_agg = 'mean','mean'
        
        x_datetime,y_datetime = '',''
        x_timeUnit,y_timeUnit = '',''

        tooltip_list = []
        print(">>>>>>>>>>>>>>>>>",data_in.printDimensions())

        for i in col_list:
            if i in data_in.printDimensions():
                col_dimensions_list.append(i)
                tooltip_list.append(i)
                all_list.append(i)
            else:
                if i[0:5] == "YEAR(":
                    col_dimensions_list.append(str(i[6:-2]) + " : Year")
                    tooltip_list.append(str(i[6:-2]) + " : Year")
                    all_list.append(str(i[6:-2]) + " : Year")
                
                elif i[0:8] == "QUARTER(":
                    col_dimensions_list.append(str(i[9:-2]) + " : Quarter")
                    tooltip_list.append(str(i[9:-2]) + " : Quarter")
                    all_list.append(str(i[9:-2]) + " : Quarter")
                    
                elif i[0:6] == "MONTH(":
                    col_dimensions_list.append(str(i[7:-2]) + " : Month")
                    tooltip_list.append(str(i[7:-2]) + " : Month")
                    all_list.append(str(i[7:-2]) + " : Month")
                    
                elif i[0:4] == "DAY(":
                    col_dimensions_list.append(str(i[5:-2]) + " : Day")
                    tooltip_list.append(str(i[5:-2]) + " : Day")
                    all_list.append(str(i[5:-2]) + " : Day")
                
                elif i[0:4] == "SUM(":
                    col_measures_list.append("sum("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("sum("+ str(i[5:-2]) + "):Q")
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])
                    
                elif i[0:4] == "AVG(":
                    col_measures_list.append("average("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("average("+ str(i[5:-2]) + "):Q")
                    #all_list.append(i[5:-2])
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])
                
                elif i[0:4] == "MED(":
                    col_measures_list.append("median("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("median("+ str(i[5:-2]) + "):Q")
                    #all_list.append(i[5:-2])
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])
                
                elif i[0:4] == "COU(":
                    col_measures_list.append("count("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("count("+ str(i[5:-2]) + "):Q")
                    #all_list.append(i[5:-2])
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])
                    
        for i in row_list:
            if i in data_in.printDimensions():
                row_dimensions_list.append(i)
                tooltip_list.append(i)
                all_list.append(i)
            else:
                if i[0:5] == "YEAR(":
                    row_dimensions_list.append(str(i[6:-2]) + " : Year:O")
                    tooltip_list.append(str(i[6:-2]) + " : Year:O")
                    all_list.append(str(i[6:-2]) + " : Year")
                
                elif i[0:8] == "QUARTER(":
                    row_dimensions_list.append(str(i[9:-2]) + " : Quarter:O")
                    tooltip_list.append(str(i[9:-2]) + " : Quarter:O")
                    all_list.append(str(i[9:-2]) + " : Quarter")
                    
                elif i[0:6] == "MONTH(":
                    row_dimensions_list.append(str(i[7:-2]) + " : Month:O")
                    tooltip_list.append(str(i[7:-2]) + " : Month:O")
                    all_list.append(str(i[7:-2]) + " : Month")
                    
                elif i[0:4] == "DAY(":
                    row_dimensions_list.append(str(i[5:-2]) + " : Day:O")
                    tooltip_list.append(str(i[5:-2]) + " : Day:O")
                    all_list.append(str(i[5:-2]) + " : Day")
                
                elif i[0:4] == "SUM(":
                    row_measures_list.append("sum("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("sum("+ str(i[5:-2]) + "):Q")
                    #all_list.append(i[5:-2])
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])
                    
                elif i[0:4] == "AVG(":
                    row_measures_list.append("average("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("average("+ str(i[5:-2]) + "):Q")
                    #all_list.append(i[5:-2])
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])
                
                elif i[0:4] == "MED(":
                    row_measures_list.append("median("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("median("+ str(i[5:-2]) + "):Q")
                    #all_list.append(i[5:-2])
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])
                
                elif i[0:4] == "COU(":
                    row_measures_list.append("count("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("count("+ str(i[5:-2]) + "):Q")
                    #all_list.append(i[5:-2])
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])



        if(col_dimensions_list == []):
            print("1")
            chart_collect = []
            if(len(row_dimensions_list) == 1):
                for i in range(len(col_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_bar().encode(
                                x=col_measures_list[i],
                                y=row_dimensions_list[0],
                                tooltip=tooltip_list
                            ).resolve_scale(
                                y='independent'
                            ).interactive()
                    chart_collect.append(chart)
            elif(len(row_dimensions_list) == 2):
                for i in range(len(col_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_bar().encode(
                                x=col_measures_list[i],
                                y=alt.Y(row_dimensions_list[1],sort=alt.SortField(field=row_dimensions_list[0],order="ascending")),
                                row=row_dimensions_list[0],
                                tooltip=tooltip_list
                            ).resolve_scale(
                                y='independent'
                            ).interactive()
                    chart_collect.append(chart)
            chart_all = alt.hconcat(*chart_collect)
            
            
        elif(row_dimensions_list == []):
            print("2")
            chart_collect = []
            if(len(col_dimensions_list) == 1):
                for i in range(len(row_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_bar().encode(
                                x=col_dimensions_list[0],
                                y=row_measures_list[i],
                                tooltip=tooltip_list
                            ).resolve_scale(
                                x='independent'
                            ).interactive()
                    chart_collect.append(chart)
            elif(len(col_dimensions_list) == 2):
                for i in range(len(row_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_bar().encode(
                                x=alt.Y(col_dimensions_list[1],sort=alt.SortField(field=col_dimensions_list[0],order="ascending")),
                                y=row_measures_list[i],
                                column=col_dimensions_list[0],
                                tooltip=tooltip_list
                            ).resolve_scale(
                                x='independent'
                            ).interactive()
                    chart_collect.append(chart)
            chart_all = alt.vconcat(*chart_collect)
        else:
            if(row_measures_list == []):
                chart_collect = []
                for i in range(len(col_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_bar().encode(
                                x=col_measures_list[i],
                                y=alt.Y(row_dimensions_list[0],sort=alt.SortField(field=row_dimensions_list[0],order="ascending")),
                                column=col_dimensions_list[0],
                                tooltip=tooltip_list
                            ).interactive()
                    chart_collect.append(chart)
                chart_all = alt.hconcat(*chart_collect)
                
            elif(col_measures_list == []):
                chart_collect = []
                for i in range(len(row_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_bar().encode(
                                x=alt.Y(col_dimensions_list[0],sort=alt.SortField(field=col_dimensions_list[0],order="ascending")),
                                y=row_measures_list[i],
                                row=row_dimensions_list[0],
                                tooltip=tooltip_list
                            ).interactive()
                    chart_collect.append(chart)
                chart_all = alt.vconcat(*chart_collect)
            
        return chart_all
    
    def LineChart(self,data_in,col_list,row_list):
        print(col_list,":",row_list)
        
        all_list = []
        col_dimensions_list = []
        row_dimensions_list = []
        col_measures_list = []
        row_measures_list = []
        col_dimensions = ''
        row_dimensions = ''
        x_measure,y_measure = '',''
        x_agg,y_agg = 'mean','mean'
        
        x_datetime,y_datetime = '',''
        x_timeUnit,y_timeUnit = '',''

        tooltip_list = []
        print(">>>>>>>>>>>>>>>>>",data_in.printDimensions())

        for i in col_list:
            if i in data_in.printDimensions():
                col_dimensions_list.append(i)
                tooltip_list.append(i)
                all_list.append(i)
            else:
                if i[0:5] == "YEAR(":
                    col_dimensions_list.append(str(i[6:-2]) + " : Year")
                    tooltip_list.append(str(i[6:-2]) + " : Year")
                    all_list.append(str(i[6:-2]) + " : Year")
                
                elif i[0:8] == "QUARTER(":
                    col_dimensions_list.append(str(i[9:-2]) + " : Quarter")
                    tooltip_list.append(str(i[9:-2]) + " : Quarter")
                    all_list.append(str(i[9:-2]) + " : Quarter")
                    
                elif i[0:6] == "MONTH(":
                    col_dimensions_list.append(str(i[7:-2]) + " : Month")
                    tooltip_list.append(str(i[7:-2]) + " : Month")
                    all_list.append(str(i[7:-2]) + " : Month")
                    
                elif i[0:4] == "DAY(":
                    col_dimensions_list.append(str(i[5:-2]) + " : Day")
                    tooltip_list.append(str(i[5:-2]) + " : Day")
                    all_list.append(str(i[5:-2]) + " : Day")
                
                elif i[0:4] == "SUM(":
                    col_measures_list.append("sum("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("sum("+ str(i[5:-2]) + "):Q")
                    all_list.append(i[5:-2])
                    
                elif i[0:4] == "AVG(":
                    col_measures_list.append("average("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("average("+ str(i[5:-2]) + "):Q")
                    all_list.append(i[5:-2])
                
                elif i[0:4] == "MED(":
                    col_measures_list.append("median("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("median("+ str(i[5:-2]) + "):Q")
                    all_list.append(i[5:-2])
                
                elif i[0:4] == "COU(":
                    col_measures_list.append("count("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("count("+ str(i[5:-2]) + "):Q")
                    all_list.append(i[5:-2])
                    
        for i in row_list:
            if i in data_in.printDimensions():
                row_dimensions_list.append(i)
                tooltip_list.append(i)
                all_list.append(i)
            else:
                if i[0:5] == "YEAR(":
                    row_dimensions_list.append(str(i[6:-2]) + " : Year:T")
                    tooltip_list.append(str(i[6:-2]) + " : Year:O")
                    all_list.append(str(i[6:-2]) + " : Year")
                
                elif i[0:8] == "QUARTER(":
                    row_dimensions_list.append(str(i[9:-2]) + " : Quarter:O")
                    tooltip_list.append(str(i[9:-2]) + " : Quarter:O")
                    all_list.append(str(i[9:-2]) + " : Quarter")
                    
                elif i[0:6] == "MONTH(":
                    row_dimensions_list.append(str(i[7:-2]) + " : Month:O")
                    tooltip_list.append(str(i[7:-2]) + " : Month:O")
                    all_list.append(str(i[7:-2]) + " : Month")
                    
                elif i[0:4] == "DAY(":
                    row_dimensions_list.append(str(i[5:-2]) + " : Day:O")
                    tooltip_list.append(str(i[5:-2]) + " : Day:O")
                    all_list.append(str(i[5:-2]) + " : Day")
                
                elif i[0:4] == "SUM(":
                    row_measures_list.append("sum("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("sum("+ str(i[5:-2]) + "):Q")
                    #all_list.append(i[5:-2])
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])
                    
                elif i[0:4] == "AVG(":
                    row_measures_list.append("average("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("average("+ str(i[5:-2]) + "):Q")
                    #all_list.append(i[5:-2])
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])
                
                elif i[0:4] == "MED(":
                    row_measures_list.append("median("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("median("+ str(i[5:-2]) + "):Q")
                    #all_list.append(i[5:-2])
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])
                
                elif i[0:4] == "COU(":
                    row_measures_list.append("count("+ str(i[5:-2]) + "):Q")
                    tooltip_list.append("count("+ str(i[5:-2]) + "):Q")
                    #all_list.append(i[5:-2])
                    if i[5:-2] in all_list:
                        continue
                    else:
                        all_list.append(i[5:-2])



        if(col_dimensions_list == []):
            print("1")
            chart_collect = []
            if(len(row_dimensions_list) == 1):
                for i in range(len(col_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_line().encode(
                                x=col_measures_list[i],
                                y=row_dimensions_list[0],
                                tooltip=tooltip_list
                            ).resolve_scale(
                                y='independent'
                            ).interactive()
                    chart_collect.append(chart)
            elif(len(row_dimensions_list) == 2):
                for i in range(len(col_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_line().encode(
                                x=col_measures_list[i],
                                y=alt.Y(row_dimensions_list[1],sort=alt.SortField(field=row_dimensions_list[0],order="ascending")),
                                row=row_dimensions_list[0],
                                tooltip=tooltip_list
                            ).resolve_scale(
                                y='independent'
                            ).interactive()
                    chart_collect.append(chart)
            chart_all = alt.hconcat(*chart_collect)
            
            
        elif(row_dimensions_list == []):
            print("2")
            chart_collect = []
            if(len(col_dimensions_list) == 1):
                for i in range(len(row_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_line().encode(
                                x=col_dimensions_list[0],
                                y=row_measures_list[i],
                                tooltip=tooltip_list
                            ).resolve_scale(
                                x='independent'
                            ).interactive()
                    chart_collect.append(chart)
            elif(len(col_dimensions_list) == 2):
                for i in range(len(row_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_line().encode(
                                x=alt.X(col_dimensions_list[1],sort=alt.SortField(col_dimensions_list[1],order="ascending")),
                                y=row_measures_list[i],
                                column=col_dimensions_list[0],
                                tooltip=tooltip_list
                            ).resolve_scale(
                                x='independent'
                            ).interactive()
                    chart_collect.append(chart)
            chart_all = alt.vconcat(*chart_collect)
        else:
            if(row_measures_list == []):
                chart_collect = []
                for i in range(len(col_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_line().encode(
                                x=col_measures_list[i],
                                y=alt.Y(row_dimensions_list[0],sort=alt.SortField(field=row_dimensions_list[0],order="ascending")),
                                column=col_dimensions_list[0],
                                tooltip=tooltip_list
                            ).interactive()
                    chart_collect.append(chart)
                chart_all = alt.hconcat(*chart_collect)
                
            elif(col_measures_list == []):
                chart_collect = []
                for i in range(len(row_measures_list)):
                    print("add Chart")
                    chart = alt.Chart(data_in.printData()[all_list]).mark_line().encode(
                                x=alt.Y(col_dimensions_list[0],sort=alt.SortField(field=col_dimensions_list[0],order="ascending")),
                                y=row_measures_list[i],
                                row=row_dimensions_list[0],
                                tooltip=tooltip_list
                            ).interactive()
                    chart_collect.append(chart)
                chart_all = alt.vconcat(*chart_collect)
            
        return chart_all
        
        """
        ############      Pie Chart
        """
    def PieChart(self,data_in,col_list,row_list,color_list,angle_list):
        print(col_list,":",row_list,":",color_list,":",angle_list)

        pie_col,pie_row = '',''
        pie_color,pie_angle = '',''
        angle_agg = 'sum'
        tooltip_list = []
        all_list = []

        for i in col_list:
            if i in data_in.printDimensions():
                pie_col = i
                tooltip_list.append(i)
                all_list.append(i)

        for i in row_list:
            if i in data_in.printDimensions():
                pie_row = i
                tooltip_list.append(i)
                all_list.append(i)

        for i in color_list:
            if i in data_in.printDimensions():
                pie_color = i
                tooltip_list.append(i)
                all_list.append(i)

        for i in angle_list:
            if i in data_in.printDimensions():
                pie_angle = i
                tooltip_list.append(i)
                all_list.append(i)
            else:
                if i[0:4] == "SUM(":
                    pie_angle = str(i[5:-2])
                    angle_agg = 'sum'
                elif i[0:4] == "AVG(":
                    pie_angle = str(i[5:-2])
                    angle_agg = 'average'
                elif i[0:4] == "MED(":
                    pie_angle = str(i[5:-2])
                    angle_agg = 'median'
                elif i[0:4] == "COU(":
                    pie_angle = str(i[5:-2])
                    angle_agg = 'count'
                tooltip_list.append(angle_agg+"("+i[5:-2]+")")
                all_list.append(i[5:-2])

        print("Col Dimension =",pie_col)
        print("Row Dimension =",pie_row)
        print("Pie Color =",pie_color)
        print("Pie Angle =",pie_angle,"Angle Agg =",angle_agg)
        print("Tooltip =",tooltip_list)

        if(pie_col == ''):
            print("1")
            chart = (alt.Chart(data_in.printData()[all_list]).mark_arc().encode(
                        theta=alt.Theta(field=pie_angle, aggregate=angle_agg),
                        color=alt.Color(field=pie_color),
                        row=alt.Row(field=pie_row),
                        tooltip=tooltip_list
                    ).resolve_scale(theta="independent",color="independent"))
        elif(pie_row == ''):
            print("2")
            chart = (alt.Chart(data_in.printData()[all_list]).mark_arc().encode(
                        theta=alt.Theta(field=pie_angle, aggregate=angle_agg),
                        color=alt.Color(field=pie_color),
                        column=alt.Column(field=pie_col),
                        tooltip=tooltip_list
                    ).resolve_scale(theta="independent",color="independent"))
        else:
            print("3")
            chart = (alt.Chart(data_in.printData()[all_list]).mark_arc().encode(
                        theta=alt.Theta(field=pie_angle, aggregate=angle_agg),
                        color=alt.Color(field=pie_color),
                        column=alt.Column(field=pie_col),
                        row=alt.Row(field=pie_row),
                        tooltip=tooltip_list
                    ).resolve_scale(theta="independent",color="independent"))
            
        return chart