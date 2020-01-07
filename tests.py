import unittest
from recourse import app, db
from mongoengine import connect
import os

class Tests(unittest.TestCase):

    def _drop_database(self):
        mongo_settings =  app.config['MONGODB_SETTINGS']
        db = connect(mongo_settings['DB'])
        db.drop_database(mongo_settings['DB'])

    def setUp(self):
        self.app = app.test_client()
        self._drop_database()

    def tearDown(self):
        self._drop_database()

    def test_alive(self):
        rv = self.app.get('/')
        assert rv.status == '200 OK'

if __name__ == '__main__':
    unittest.main()
