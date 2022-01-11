import unittest
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import api
    

class MyTestCase(unittest.TestCase):

    def setUp(self):
        api.app.testing = True
        self.app = api.app.test_client()
        
    # response is 200
    def test_index(self):
        response = self.app.get("/houses")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        
    # content return is application/json
    def test_index_content(self):
        response = self.app.get("/houses")
        self.assertEqual(response.content_type, "application/json")

    # data returned
    def test_index_data(self):
        response = self.app.get("/houses")
        self.assertTrue(b"Message" in response.data)
        
        
if __name__ == "__main__":
    unittest.main()
