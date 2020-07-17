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
