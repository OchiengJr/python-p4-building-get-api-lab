import json
import unittest  # Assuming use of unittest framework for organizing tests
from app import app, db
from models import Bakery, BakedGood

class TestBakeryAPI(unittest.TestCase):
    '''Test cases for Bakery API endpoints.'''

    @classmethod
    def setUpClass(cls):
        '''Setup any state specific to the execution of the class.'''
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.json.compact = False
        db.init_app(app)
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        '''Teardown any state that was previously setup.'''
        with app.app_context():
            db.drop_all()

    def setUp(self):
        '''Setup run before every test method.'''
        self.client = app.test_client()

    def tearDown(self):
        '''Teardown run after every test method.'''
        with app.app_context():
            db.session.rollback()

    def test_bakeries_route(self):
        '''Test if "/bakeries" endpoint returns status code 200.'''
        response = self.client.get('/bakeries')
        self.assertEqual(response.status_code, 200)

    def test_bakeries_route_returns_json(self):
        '''Test if "/bakeries" endpoint returns JSON content type.'''
        response = self.client.get('/bakeries')
        self.assertEqual(response.content_type, 'application/json')

    def test_bakeries_route_returns_list_of_bakeries(self):
        '''Test if "/bakeries" endpoint returns a list of Bakery objects.'''
        with app.app_context():
            bakery = Bakery(name="My Bakery")
            db.session.add(bakery)
            db.session.commit()

            response = self.client.get('/bakeries')
            data = json.loads(response.data.decode())
            self.assertIsInstance(data, list)
            self.assertTrue(any(b['name'] == 'My Bakery' for b in data))

    # Additional tests for other endpoints can follow similar structure

if __name__ == '__main__':
    unittest.main()

