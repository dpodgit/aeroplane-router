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

class Airport:

   def __init__(self, data_store, airport_code):
      self._airport_code = airport_code
      self._data = data_store

      try:
         self._airport_name,\
         self._latitude,\
         self._longitude,\
         self._country,\
         self._currency,\
         self._to_euro_rate = self._populate_fields(self._airport_code)

      except:
         print("An Airport not found.\nQuitting")

   def _populate_fields(self, code):
      """Using airport's identifying code, looks up relevant data and returns to
      instance's attributes. Called from init method. 'country' in first loop is
      used internally to search, in the second loop, for the currency ('found_currency')
      in that country, from within a different dictionary. This latter value is
      used in turn, in the third loop, to search again a different dictionary for
      the exchange rate to Euro for that airport's country's currency.

      Parameters
      ----------
      code: string
         An airport's identifying string
      """
      try:
         for key in self._data._airport_dict:
            if self._data._airport_dict[key]['airport_code'] == code:
               self._found_airport_name = self._data._airport_dict[key]['airport_name']
               self._found_latitude = self._data._airport_dict[key]['latitude']
               self._found_longitude = self._data._airport_dict[key]['longitude']
               self._found_country = self._data._airport_dict[key]['country']
               break

         for key in self._data._countrycurrency_dict:
            if self._data._countrycurrency_dict[key]['currency_country_name'] \
               == self._found_country.upper():
               self._found_currency = self._data._countrycurrency_dict[key]['currency_alphabetic_code']
               break

         for key in self._data._currency_rates_dict:
            if self._data._currency_rates_dict[key]['CurrencyCode'] == self._found_currency:
               self._found_to_euro_rate = self._data._currency_rates_dict[key]['toEuro']
               break

         return self._found_airport_name,\
               float(self._found_latitude),\
               float(self._found_longitude),\
               self._found_country,\
               self._found_currency,\
               self._found_to_euro_rate

      except:
         print("An Error Has Occurred Populating Airport Fields.\nQuitting")
         sys.exit()
