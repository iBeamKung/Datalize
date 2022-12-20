from pkgutil import get_data
import unittest
import pandas as pd

import data
        
class DataTestCase(unittest.TestCase):
    def setUp(self):
        self.df = data.dataSource()
        self.df.importData("testfile01_csv.csv")

    def test_printDimensions(self):
        self.assertIsInstance(self.df.printDimensions(),list)
        
    def test_printDatetime(self):
        self.assertIsInstance(self.df.printDatetime(),list)
        
    def test_printMeasures(self):
        self.assertIsInstance(self.df.printMeasures(),list)
        
    def test_filtersData(self):
        data = self.df.filtersData("firstname",["Beam"])
        getdata = self.df.rowDisplay()
        self.assertEqual(getdata,5)
        
        data = self.df.filtersData("firstname",["Beam","Gap"])
        getdata = self.df.rowDisplay()
        self.assertEqual(getdata,9)
        
    def test_filtersMeasures(self):
        data = self.df.filtersMeasures("score",[13,84])
        getdata = self.df.printMaxValue("score")
        self.assertEqual(getdata,80)
        getdata = self.df.printMinValue("score")
        self.assertEqual(getdata,13)
        
    def test_filtersDate(self):
        data = self.df.filtersDate("exam date",[2022])
        getdata = self.df.rowDisplay()
        self.assertEqual(getdata,17)
        
    def test_printMaxValueOG(self):
        data = self.df.filtersMeasures("score",[13,84])
        getdata = self.df.printMaxValueOG("score")
        self.assertEqual(getdata,94)
        
    def test_printMinValueOG(self):
        data = self.df.filtersMeasures("score",[13,84])
        getdata = self.df.printMinValueOG("score")
        self.assertEqual(getdata,1)
        
    def test_printDimensions(self):
        getdata = self.df.printDimensions()
        print(getdata)
        self.assertListEqual(getdata,["row id","firstname","subject"])
        
    def test_printDatetime(self):
        getdata = self.df.printDatetime()
        self.assertListEqual(getdata,["exam date"])
        
    def test_printMeasures(self):
        getdata = self.df.printMeasures()
        self.assertListEqual(getdata,["score"])
        
    def test_colDisplay(self):
        getdata = self.df.colDisplay()
        self.assertEqual(getdata,5)
        
    def test_rowDisplay(self):
        getdata = self.df.rowDisplay()
        self.assertEqual(getdata,20)
        
    def test_maxValue(self):
        getdata = self.df.printMaxValue("score")
        self.assertEqual(getdata,94)
        
    def test_minValue(self):
        getdata = self.df.printMinValue("score")
        self.assertEqual(getdata,1)
        
    def test_add_data(self):
        self.add_data = data.dataSource()
        self.add_data.importData("addfile01_csv.csv")
        self.assertEqual(self.add_data.rowDisplay(),10)
        
        self.add_data.addData("addfile02_csv.csv")
        self.assertEqual(self.add_data.rowDisplay(),20)
        
    def test_group_sum(self):
        data_handler = data.dataHandler(self.df.printData())
        getdata = data_handler.group(["firstname"],["SUM( score )"])
        beam_data = getdata.loc[getdata["firstname"]=="Beam","score: SUM"].values[0]
        gap_data = getdata.loc[getdata["firstname"]=="Gap","score: SUM"].values[0]
        self.assertEqual(beam_data,242)
        self.assertEqual(gap_data,110)
        
    def test_group_avg(self):
        data_handler = data.dataHandler(self.df.printData())
        getdata = data_handler.group(["firstname"],["AVG( score )"])
        beam_data = getdata.loc[getdata["firstname"]=="Beam","score: AVG"].values[0]
        gap_data = getdata.loc[getdata["firstname"]=="Gap","score: AVG"].values[0]
        self.assertEqual(beam_data,48.4)
        self.assertEqual(gap_data,27.5)
        
    def test_group_count(self):
        data_handler = data.dataHandler(self.df.printData())
        getdata = data_handler.group(["firstname"],["COU( score )"])
        beam_data = getdata.loc[getdata["firstname"]=="Beam","score: Count"].values[0]
        gap_data = getdata.loc[getdata["firstname"]=="Gap","score: Count"].values[0]
        self.assertEqual(beam_data,5)
        self.assertEqual(gap_data,4)

if __name__ == '__main__':
   unittest.main()