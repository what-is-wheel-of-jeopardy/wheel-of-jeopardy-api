import unittest
from api.pre_game import app
import json

# Common function to convert bytes to string and trim empty space
def to_str(s):
    return str(s, 'utf-8').strip()

class API_test(unittest.TestCase):
    # Test get all categories API endpoint(GET)
    def test_show_cats(self):
        tester = app.test_client(self)
        res = tester.get('/admin/show_cats', content_type='application/json')
        self.assertEqual(res.status_code, 200)
        # self.assertEqual(to_str(res.data), '[{"id":7,"name":"Geography"},{"id":12,"name":"Sports and Entertainment"},{"id":11,"name":"Solar System"},{"id":9,"name":"Religion"},{"id":8,"name":"Science"},{"id":10,"name":"History"}]')

    # Test update existing category name API endpoint(POST)
    # def test_update_category(self):
    #     tester = app.test_client(self)
    #     res = tester.post('/admin/update_cat/10', 
    #                     data=json.dumps({'name': 'History'}),
    #                     follow_redirects=False)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(to_str(res.data), '"Category updated: History"')

    # Test get all Q and A by category_id API endpoint(GET)
    def test_show_QA_by_cat_id(self):
        tester = app.test_client(self)
        res = tester.get('/admin/show_qas/10', content_type='application/json')
        self.assertEqual(res.status_code, 200)
        # self.assertEqual(to_str(res.data), '[{"answer":"George Washington","category_id":10,"id":52,"question":"Who was the 1st president of Unites States","score":"200"},{"answer":"1776","category_id":10,"id":53,"question":"In which year did USA gain independence ","score":"400"},{"answer":"Japan","category_id":10,"id":55,"question":"Which country is the home of Samurai ?","score":"800"},{"answer":"Istanbul","category_id":10,"id":56,"question":"In 1923 what was Constantinopole renamed into?","score":"1000"},{"answer":"Nelson Mandela","category_id":10,"id":54,"question":"Which south african president was jailed for 27 years?","score":"600"}]')

if __name__ == '__main__':
    unittest.main()