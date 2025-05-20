import unittest, requests


def make_request(entity, body):
    base_url = "http://10.15.1.125:8081/" + entity
    response = requests.post(f'{base_url}', body)
    return response


class MyTestCase(unittest.TestCase):
    def test_post_amistades(self):
        # Act:
        body = '{"usuario_id": 4, "amistad_id": 10}'
        response = make_request('amistades', body)
        status_code = response.status_code
        data = response.json()
        print(data)
        self.assertEqual(201, status_code)  # add assertion here


if __name__ == '__main__':
    unittest.main()
