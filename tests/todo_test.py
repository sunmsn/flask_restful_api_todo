import unittest
import requests


class TodoTestCase(unittest.TestCase):
    def test_todo_post(self):
        # test 1
        payload = {
            'content': "test1",
            'state': 'finished'
        }
        r = requests.post('http://127.0.0.1:5000/api/v1.0/todo', data=payload)
        self.assertTrue(r.status_code == 201)
        # test 2
        payload = {
            'content': "test2",
        }
        r = requests.post('http://127.0.0.1:5000/api/v1.0/todo', data=payload)
        self.assertTrue(r.status_code == 201)
        # test 3
        payload = {
            'content': "",
            'state': 'finished'
        }
        r = requests.post('http://127.0.0.1:5000/api/v1.0/todo', data=payload)
        self.assertTrue(r.status_code == 400)
        # test 4
        payload = {
            'content': "test3",
            'state': '1234567890'
        }
        r = requests.post('http://127.0.0.1:5000/api/v1.0/todo', data=payload)
        self.assertTrue(r.status_code == 201)
        # test 5
        payload = {
            'content': "test4",
            'state': '12345678901'
        }
        r = requests.post('http://127.0.0.1:5000/api/v1.0/todo', data=payload)
        self.assertTrue(r.status_code == 400)
        # test 6
        payload = {
            'content': "abcdefghijklmnopqrstuvwxy",
            'state': '1234567890'
        }
        r = requests.post('http://127.0.0.1:5000/api/v1.0/todo', data=payload)
        self.assertTrue(r.status_code == 201)
        # test 7
        payload = {
            'content': "abcdefghijklmnopqrstuvwxyz",
            'state': '1234567890'
        }
        r = requests.post('http://127.0.0.1:5000/api/v1.0/todo', data=payload)
        self.assertTrue(r.status_code == 400)
        # test 8
        payload = {
            'state': '1234567890'
        }
        r = requests.post('http://127.0.0.1:5000/api/v1.0/todo', data=payload)
        self.assertTrue(r.status_code == 400)

    def test_todo_get(self):
        r = requests.get('http://127.0.0.1:5000/api/v1.0/todo')
        self.assertTrue(r.status_code == 200)

    def test_doto_detail_get(self):
        # prepare
        payload = {
            'content': "test1",
            'state': 'finished'
        }
        r = requests.post('http://127.0.0.1:5000/api/v1.0/todo', data=payload)
        self.assertTrue(r.status_code == 201)
        # test get
        i = 1
        while True:
            url = 'http://127.0.0.1:5000/api/v1.0/todo/' + str(i)
            i = i + 1
            r = requests.get(url)
            if r.status_code == 200:
                break
        r = requests.get(url)
        self.assertTrue(r.status_code == 200)

    def test_doto_detail_delete(self):
        # prepare
        payload = {
            'content': "test1",
            'state': 'finished'
        }
        r = requests.post('http://127.0.0.1:5000/api/v1.0/todo', data=payload)
        self.assertTrue(r.status_code == 201)
        i = 1
        while True:
            url = 'http://127.0.0.1:5000/api/v1.0/todo/' + str(i)
            i = i + 1
            r = requests.get(url)
            if r.status_code == 200:
                break
        # test delete
        r = requests.delete(url)
        self.assertTrue(r.status_code == 204)
        r = requests.delete(url)
        self.assertTrue(r.status_code == 404)
        r = requests.get(url)
        self.assertTrue(r.status_code == 404)


    def test_doto_detail_put(self):
        # prepare
        payload = {
            'content': "test1",
            'state': 'finished'
        }
        r = requests.post('http://127.0.0.1:5000/api/v1.0/todo', data=payload)
        self.assertTrue(r.status_code == 201)
        i = 1
        while True:
            url = 'http://127.0.0.1:5000/api/v1.0/todo/' + str(i)
            i = i + 1
            r = requests.get(url)
            if r.status_code == 200:
                break
        # test 1
        payload = {
            'content': "old_test",
            'state': 'old'
        }
        r = requests.put(url, data=payload)
        self.assertTrue(r.status_code == 201)
        r = requests.get(url)
        self.assertTrue(r.json()['content'] == "old_test")
        self.assertTrue(r.json()['state'] == 'old')
        # test 2
        payload = {
            'content': "new_test"
        }
        r = requests.put(url, data=payload)
        self.assertTrue(r.status_code == 201)
        r = requests.get(url)
        self.assertTrue(r.json()['content'] == "new_test")
        self.assertTrue(r.json()['state'] == 'old')
        # test 3
        payload = {
            'state': 'new'
        }
        r = requests.put(url, data=payload)
        self.assertTrue(r.status_code == 201)
        r = requests.get(url)
        self.assertTrue(r.json()['content'] == "new_test")
        self.assertTrue(r.json()['state'] == 'new')
        # test 4
        payload = {
        }
        r = requests.put(url, data=payload)
        self.assertTrue(r.status_code == 201)
        r = requests.get(url)
        self.assertTrue(r.json()['content'] == "new_test")
        self.assertTrue(r.json()['state'] == 'new')
        # test 5
        payload = {
            'content': "",
            'state': 'old'
        }
        r = requests.put(url, data=payload)
        self.assertTrue(r.status_code == 400)
        # test 6
        payload = {
            'content': "old_test",
            'state': '12345678901'
        }
        r = requests.put(url, data=payload)
        self.assertTrue(r.status_code == 400)
        # test 7
        payload = {
            'content': "abcdefghijklmnopqrstuvwxyz",
            'state': 'old'
        }
        r = requests.put(url, data=payload)
        self.assertTrue(r.status_code == 400)


suite = unittest.TestSuite()
suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TodoTestCase))
unittest.TextTestRunner().run(suite)
