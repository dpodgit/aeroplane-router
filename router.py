"""
@author: David O'Dwyer
Created: 2019
"""

import os
import sys
import csv
import glob

class Data:

   def __init__(self):
      self._input_csvs = Data._collect_datasets()
      self._input_test = ''.join([item for item in self._input_csvs if \
                           os.path.basename(item) == 'test.csv'])
      self._input_csvs.remove(self._input_test)

      self._aircraft_dict = dict()
      self._airport_dict = dict()
      self._countrycurrency_dict = dict()
      self._currency_rates_dict = dict()

      self._output_dicts = [self._aircraft_dict,
                           self._airport_dict,
                           self._countrycurrency_dict,
                           self._currency_rates_dict]

   def _collect_datasets():
      """Returns the absolute path for each .csv path in the hard-coded path.
      """
      csv_repo = \
      "/Users/davidodwyer/Documents/computerScience/Independent/scripts/python-scripts/aeroplane_routing" 

      try:
         filepaths = [os.path.abspath(f) for f in os.listdir(path=csv_repo)\
            if '.csv' in os.path.basename(f)]
         return filepaths
      except:
         print("Dataset Collection Failed.\nQuitting")
         sys.exit()

   def populate_dicts(self):
      """Opens, reads, and writes to prior initialised dictionaries, positionally
      ordered in the _output_dicts, the 4 informational / non-test csv files. 
      Hard-coded loop, as always only 4 such files.
      """
      try:
         iteration = 0 # outer iteration indexes a dict from _output dicts 
         while iteration < 4:
            with open(self._input_csvs[iteration], newline='') as csv_file:
               csv_reader = csv.DictReader(csv_file)

               i=0 # incrememting variables used to set dict key for each row
               for row in csv_reader:
                  self._output_dicts[iteration][i] = dict(row)
                  i+=1

            iteration+=1

      except:
         print("Reading CSVs Failed.\nQuitting")
         sys.exit()

class Aircraft:

   def __init__(self, data_store, aircraft_code):
      self._aircraft_code = aircraft_code
      self._data = data_store
      self._range = self._lookup_range(self._aircraft_code)

   def _lookup_range(self, code):
      """ Sets aircraft's _range attribute with normalised range (km), which is 
      looked up in the _aircraft_dict. Finds key where code == code; uses key 
      to access that entry's range value. Called from Class' init method.

      Parameters
      ----------
      code: string
         Identifying aircraft code, which is first passed to the init method.
      """
      try:
         for key in self._data._aircraft_dict:
            if self._data._aircraft_dict[key]['code'] == code:
               self._found_range = float(self._data._aircraft_dict[key]['range'])
               self._metric = self._data._aircraft_dict[key]['units']
               if self._metric.lower().strip() == 'imperial':
                  self._found_range =  self._found_range * 1.60934
               
               return self._found_range
      except KeyError:
         print("An Aircraft Code Was Not Found.\nQuitting")
         sys.exit()