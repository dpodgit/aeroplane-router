"""
@author: David O'Dwyer
Created: 2019
"""

import os
import sys
import csv
import glob
from itertools import permutations
from math import sin, cos, radians, asin, sqrt

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

class Router:

   def __init__(self, data_store):

      self._aircraft_dict = dict()
      self._airport_dict = dict()
      self._data = data_store

   def _calculate_distance(self, airport1, airport2):
      """A method that return the great circle distance (shortest distance between
      two points on the surface of a sphere), which is calculated using the
      Haversine formula.

      Parameters
      ----------
      airport1: Airport instance
         The first of two airports to measure the disance between

      airport2: Airport instance
         The second of two airports to measure the disance between
      """

      lat1 = airport1._latitude
      lon1 = airport1._longitude
      lat2 = airport2._latitude
      lon2 = airport2._longitude

      R = 6372.8

      dlat = radians(lat2 - lat1)
      dlon = radians(lon2 - lon1)
      lat1 = radians(lat1)
      lat2 = radians(lat2)

      a = sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
      c = 2 * asin(sqrt(a))

      return c * R

   def load_row(self, row):
      """A method that takes a row (passed by main) and creates airport and 
      aircraft objects corresponding to the identifying strings contained in the 
      row. It checks whether the objects exist in the cache before creating. It
      adds created objects to the cache upon creating them.

      Parameters
      ----------
      row: list
         A list of strings, e.g. ['DUB', 'LHR', 'CDG', 'AMS', 'CPH', 'SIS99']
         Last element is airport. First element is "home" airport. Remaining
         elements are intermediary airports.
      """
      self._row = row

      # check by aircraft code if aircraft in cache; create & add otherwise

      if self._row[5] in self._aircraft_dict:
         self._aircraft = self._aircraft_dict[self._row[5]]
      else:
         self._aircraft = Aircraft(self._data, self._row[5])
         self._aircraft_dict[self._row[5]] = self._aircraft
               
      # check by airport code if airport in cache; create & add otherwise
      # add airports to list, for _generate_permutations method

      self._airports = [None,
                        None,
                        None,
                        None,
                        None] #placeholders, index 0 is home airport; 1-3 inc. are destinations

      for i in range(len(self._airports)):
         if self._row[0:5][i] in self._airport_dict:
            self._airports[i] = self._airport_dict[self._row[0:5][i]]
            
         else:
            self._airports[i] = Airport(self._data, self._row[0:5][i])
            self._airports[i]._populate_fields(self._data)
            self._airport_dict[self._row[0:5][i]] = self._airports[i]

   def _generate_permutations(self):
      """A method that generates permutations of all aircraft, excluding the 
      first "home" airport.
      """

      self._permutations = [list(airport) for airport in list(permutations(self._airports[1:5]))]

   def add_cost_add_flag(self):
      """A method that firstly generates the permutations. Secondly, iterates through
      a permutation and calculates the distance and cost of each intermediary
      journey (i.e. excluding home airport —> first destination, and final
      destination —> home airport). Thirdly, adds the distance and cost of the 
      first leg (home airport —> first destination). Fourthly, adds the distance
      and cost of the last leg (final destination —> home airport). The total 
      cost of the round trip is appended to the permutation / list. If no leg of
      round trip exceeds the aircraft range, None is appended to the list. If a
      leg does exceed the range, False is appended in place of None. Repeated
      for each permutation in the _permutations list.
      """

      self._generate_permutations()

      for journey in self._permutations:
         flag = None
         total_distance = 0
         cost = 0

         # tally distance & cost for all except outset & ending journeys
         for i in range(len(journey)-1):
            distance = self._calculate_distance(journey[i], journey[i+1])
            total_distance += distance
            if distance > self._aircraft._range:
               flag = False
            cost += (distance * float(journey[i]._to_euro_rate))

         # add distance for the first leg of the journey
         distance = self._calculate_distance(self._airports[0], journey[0])
         total_distance += distance
         if distance > self._aircraft._range:
            flag = False
         cost += (distance * float(self._airports[0]._to_euro_rate))

         # add distance for the final leg of journey
         distance = self._calculate_distance(self._airports[0], journey[-1])
         total_distance += distance
         if distance > self._aircraft._range:
            flag = False
         cost += (distance * float(journey[-1]._to_euro_rate))

         journey.append(round(cost, 2))
         journey.append(flag)

   def return_cheapest_route(self):
      """A method that first sets the lowest price by iterating through all
      valid permuted routes. Secondly, linearally searches for the journey
      matching that lowest price. Returns the home airport, and the lowest-
      price journey.
      """
      lowest_price = 999_999_999

      for journey in self._permutations:
         if not journey[-1] == False:
            if journey[-2] < lowest_price:
               lowest_price = journey[-2]
      
      for journey in self._permutations:
         if journey[-2] != lowest_price:
            continue
         return self._airports[0], journey

def main():
   """
   Driver function. Initialises and prepares Data and Router instances.
   Opens the test csv file via the Data instance's attribute, and generates a 
   cheapest route for each line / journey. Prints formatted output of each 
   best journey to terminal.
   """

   inputs = Data()
   router = Router(inputs)

   inputs.populate_dicts()

   result = """
   Starting Airport:     {0}
   Destination airports: {1}

   Best route: {2}  —>  {3}  —>  {4}  —>  {5}  —>  {6}  —>  {2}

   Cost:           E {7}

   __________________________________________________

   """

   with open (inputs._input_test) as file:
      reader = csv.reader(file)
      next(reader)
      for row in reader:
         router.load_row(row)
         router.add_cost_add_flag()
         best_route = router.return_cheapest_route()

         # tuple best route first element: home airport
         # present latter beginning and end, as home —> 1st destination
         # and last desination —> home are factored in in Router.add_cost_add_flag
         print(result.format( row[0],
                              ', '.join(row[1:5]),
                              best_route[0]._airport_code,
                              best_route[1][0]._airport_code,
                              best_route[1][1]._airport_code,
                              best_route[1][2]._airport_code,
                              best_route[1][3]._airport_code,
                              best_route[1][4]))

if __name__ == "__main__":
   main()