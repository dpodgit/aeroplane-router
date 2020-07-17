import unittest
import aeroplane_router as prog

class Test(unittest.TestCase):

   def setUp(self):
      self._inputs = prog.Data()
      self._router = prog.Router(self._inputs)
      self._inputs.populate_dicts()

      self._aircraft = prog.Aircraft(self._inputs, 'F50')
      self._aircraft2 = prog.Aircraft(self._inputs, 'MD11')

      self._airport = prog.Airport(self._inputs, 'AMS')
      self._airport2 = prog.Airport(self._inputs, 'DUB')

   def tearDown(self):
      pass

   def test_aircraft_range_lookup(self):
      self.assertEqual(self._aircraft._range, 2055.0)
      self.assertEqual(self._aircraft2._range, 20390.3378)

   def test_airport_lookup(self):
      self.assertEqual(self._airport._airport_name, 'Schiphol')
      self.assertEqual(self._airport._latitude, 52.308613)
      self.assertEqual(self._airport._longitude, 4.763889)
      self.assertEqual(self._airport._country, 'Netherlands')
      self.assertEqual(self._airport._currency, 'EUR')
      self.assertEqual(self._airport._to_euro_rate, '1')

   def test_airport_distance(self):
      self.assertEqual(self._router._calculate_distance(self._airport, self._airport2), 750.3717994608915)


if __name__ == "__main__":
    unittest.main(verbosity=2)

