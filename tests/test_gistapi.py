import unittest
from unittest.mock import patch, MagicMock

from gistapi import app


class GistAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_ping(self):
        response = self.app.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'pong')

    @patch('gistapi.requests.get')
    def test_search_valid_data(self, mock_get):
        mock_gists_for_user = MagicMock()
        mock_gists_for_user.status_code = 200
        mock_gists_for_user.json.return_value = [
            {
                'url': 'https://api.github.com/gists/test_gist',
                'id': 'test_gist',
                'html_url': 'https://gist.github.com/test_gist'
            }
        ]

        mock_gist_content = MagicMock()
        mock_gist_content.status_code = 200
        mock_gist_content.json.return_value = {
            'files': {
                'file1.py': {
                    'raw_url': 'https://gist.githubusercontent.com/raw/file1.py'
                }
            },
            'id': 'test_gist',
            'html_url': 'https://gist.github.com/test_gist'
        }

        mock_raw_content = MagicMock()
        mock_raw_content.status_code = 200
        mock_raw_content.text = 'import requests'

        mock_get.side_effect = [
            mock_gists_for_user,
            mock_gist_content,
            mock_raw_content
        ]

        with app.test_request_context():
            data = {'username': 'testuser', 'pattern': 'import requests'}
            response = self.app.post('/api/v1/search', json=data)
            self.assertEqual(response.status_code, 200)

            json_resp = response.get_json()
            self.assertEqual(json_resp['status'], 'success')
            self.assertGreater(len(json_resp['matches']), 0)

    @patch('gistapi.requests.get')
    def test_search_invalid_username(self, mock_get):
        mock_gists_for_user = MagicMock()
        mock_gists_for_user.status_code = 404
        mock_get.return_value = mock_gists_for_user

        with app.test_request_context():
            data = {'username': 'invaliduser', 'pattern': 'import requests'}
            response = self.app.post('/api/v1/search', json=data)
            self.assertEqual(response.status_code, 400)

            json_resp = response.get_json()
            self.assertEqual(json_resp['status'], 'error')

    @patch('gistapi.requests.get')
    def test_search_no_matches(self, mock_get):
        mock_gists_for_user = MagicMock()
        mock_gists_for_user.status_code = 200
        mock_gists_for_user.json.return_value = [
            {'url': 'https://api.github.com/gists/test_gist', 'id': 'test_gist',
             'html_url': 'https://gist.github.com/test_gist'}
        ]
        mock_gist_content = MagicMock()
        mock_gist_content.status_code = 200
        mock_gist_content.json.return_value = {
            'files': {
                'file1.py': {
                    'raw_url': 'https://gist.githubusercontent.com/raw/file1.py'
                }
            },
            'id': 'test_gist',
            'html_url': 'https://gist.github.com/test_gist'
        }
        mock_raw_content = MagicMock()
        mock_raw_content.status_code = 200
        mock_raw_content.text = 'print("Hello, world!")'

        mock_get.side_effect = [
            mock_gists_for_user,
            mock_gist_content,
            mock_raw_content
        ]

        with app.test_request_context():
            data = {'username': 'testuser', 'pattern': 'import requests'}
            response = self.app.post('/api/v1/search', json=data)
            self.assertEqual(response.status_code, 200)

            json_resp = response.get_json()
            self.assertEqual(json_resp['status'], 'success')
            self.assertEqual(len(json_resp['matches']), 0)

    def test_search_missing_username(self):
        data = {'pattern': 'import requests'}
        response = self.app.post('/api/v1/search', json=data)
        self.assertEqual(response.status_code, 400)

        json_resp = response.get_json()
        self.assertEqual(json_resp['status'], 'error')
        self.assertEqual(json_resp['message'], 'Invalid or missing username')

    def test_search_missing_pattern(self):
        data = {'username': 'testuser'}
        response = self.app.post('/api/v1/search', json=data)
        self.assertEqual(response.status_code, 400)
        json_resp = response.get_json()

        self.assertEqual(json_resp['status'], 'error')
        self.assertEqual(json_resp['message'], 'Invalid or missing pattern')
