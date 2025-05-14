import unittest
import requests


def make_request(entity):
    base_url = "http://192.168.0.243:8081/" + entity
    response = requests.get(f'{base_url}')
    return response


class MyTestCase(unittest.TestCase):
    def test_get_usuarios(self):
        # Act:
        response = make_request('usuarios')
        status_code = response.status_code
        data = response.json()
        self.assertEqual(200, status_code)  # add assertion here
        self.assertGreaterEqual(len(data), 10)

    def test_get_highlight(self):
        # Act:
        response = make_request('highlights')
        status_code = response.status_code
        data = response.json()
        self.assertEqual(200, status_code)  # add assertion here
        self.assertGreaterEqual(len(data), 10)

    def test_get_productos(self):
        # Act:
        response = make_request('productos')
        status_code = response.status_code
        data = response.json()
        self.assertEqual(200, status_code)  # add assertion here
        self.assertGreaterEqual(len(data), 10)

    def test_get_categorias(self):
        # Act:
        response = make_request('categorias')
        status_code = response.status_code
        data = response.json()
        self.assertEqual(200, status_code)  # add assertion here
        self.assertGreaterEqual(len(data), 10)

    def test_get_amistades(self):
        # Act:
        response = make_request('amistades')
        status_code = response.status_code
        data = response.json()
        self.assertEqual(200, status_code)  # add assertion here
        self.assertGreaterEqual(len(data), 10)

    def test_get_eventos(self):
        # Act:
        response = make_request('eventos')
        status_code = response.status_code
        data = response.json()
        self.assertEqual(200, status_code)  # add assertion here
        self.assertGreaterEqual(len(data), 10)

    def test_get_reviews(self):
        # Act:
        response = make_request('reviews')
        status_code = response.status_code
        data = response.json()
        self.assertEqual(200, status_code)  # add assertion here
        self.assertGreaterEqual(len(data), 10)

    def test_get_ordenes(self):
        # Act:
        response = make_request('ordenes')
        status_code = response.status_code
        data = response.json()
        self.assertEqual(200, status_code)  # add assertion here
        self.assertGreaterEqual(len(data), 10)

    def test_get_compartidos(self):
        # Act:
        response = make_request('compartidos')
        status_code = response.status_code
        data = response.json()
        self.assertEqual(200, status_code)  # add assertion here
        self.assertGreaterEqual(len(data), 10)


if __name__ == '__main__':
    unittest.main()
