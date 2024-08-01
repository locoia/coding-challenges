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
        mock_raw_content.iter_content = MagicMock(return_value=[b'import requests'])

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
            data = {'username': None, 'pattern': 'import requests'}
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
        mock_raw_content.text = MagicMock(return_value=[b'Text not matching'])

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

    @patch('gistapi.requests.get')
    def test_search_with_pagination(self, mock_get):
        mock_gists_for_user_page1 = MagicMock()
        mock_gists_for_user_page1.status_code = 200
        mock_gists_for_user_page1.json.return_value = [
            {'url': 'https://api.github.com/gists/test_gist1', 'id': 'test_gist1',
             'html_url': 'https://gist.github.com/test_gist1'}
        ]
        mock_gists_for_user_page1.headers = {
            'Link': '<https://api.github.com/users/testuser/gists?page=2>; rel="next"'
        }

        mock_gists_for_user_page2 = MagicMock()
        mock_gists_for_user_page2.status_code = 200
        mock_gists_for_user_page2.json.return_value = [
            {'url': 'https://api.github.com/gists/test_gist2', 'id': 'test_gist2',
             'html_url': 'https://gist.github.com/test_gist2'}
        ]
        mock_gists_for_user_page2.headers = {
            'Link': '<https://api.github.com/users/testuser/gists?page=3>; rel="next"'
        }

        mock_gists_for_user_page3 = MagicMock()
        mock_gists_for_user_page3.status_code = 200
        mock_gists_for_user_page3.json.return_value = []
        mock_gists_for_user_page3.headers = {}

        mock_gist_content_response1 = MagicMock()
        mock_gist_content_response1.status_code = 200
        mock_gist_content_response1.json.return_value = {
            'files': {
                'file1.py': {
                    'raw_url': 'https://gist.githubusercontent.com/raw/file1.py'
                }
            },
            'id': 'test_gist1',
            'html_url': 'https://gist.github.com/test_gist1'
        }

        mock_gist_content_response2 = MagicMock()
        mock_gist_content_response2.status_code = 200
        mock_gist_content_response2.json.return_value = {
            'files': {
                'file2.py': {
                    'raw_url': 'https://gist.githubusercontent.com/raw/file2.py'
                }
            },
            'id': 'test_gist2',
            'html_url': 'https://gist.github.com/test_gist2'
        }

        mock_raw_content_response1 = MagicMock()
        mock_raw_content_response1.status_code = 200
        mock_raw_content_response1.iter_content = MagicMock(return_value=[b'import requests'])
        mock_raw_content_response2 = MagicMock()
        mock_raw_content_response2.status_code = 200
        mock_raw_content_response2.iter_content = MagicMock(return_value=[b'import requests'])

        # Order of requests.get calls
        mock_get.side_effect = [
            mock_gists_for_user_page1,
            mock_gists_for_user_page2,
            mock_gists_for_user_page3,
            mock_gist_content_response1,
            mock_raw_content_response1,
            mock_gist_content_response2,
            mock_raw_content_response2,
        ]

        with app.test_request_context():
            data = {'username': 'testuser', 'pattern': 'import requests'}
            response = self.app.post('/api/v1/search', json=data)
            self.assertEqual(response.status_code, 200)

            json_resp = response.get_json()
            self.assertEqual(json_resp['status'], 'success')
            self.assertEqual(len(json_resp['matches']), 2)
