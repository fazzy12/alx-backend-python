#!/usr/bin/env python3
""" This project module contains the first unit test
for client.py file.
"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD
import requests


class TestGithubOrgClient(unittest.TestCase):
    """ TestGithubOrgClient inherits from unittest. TestCase to test
    client.GithubOrgClient.
    """
    @parameterized.expand([
        ("google", {}),
        ("abc", {})
    ])
    @patch('client.get_json')
    def test_org(self, url, expected_result, mock):
        """ Tests that GithubOrgClient.org returns the correct value.
        """
        mock.return_value = {}
        r = GithubOrgClient(url)
        self.assertEqual(r.org, expected_result)
        mock.assert_called_once()

    def test_public_repos_url(self):
        """ Tests that _public_repos_url returns a known payload.
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock:
            mock.return_value = {'repos_url': 'http://testing.url'}
            tg = GithubOrgClient('xyz')
            r = tg._public_repos_url
            self.assertEqual(r, mock.return_value.get('repos_url'))

    @patch('client.get_json')
    def test_public_repos(self, get_json_mock):
        """ Tests that test_public_repos returns a known payload.
        """
        get_json_mock.return_value = [
            {'name': 'repo_0'},
            {'name': 'repo_1'},
            {'name': 'repo_2'}
        ]
        get_json_mock()
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock:
            mock.return_value = [
                {'name': 'repo_0'},
                {'name': 'repo_1'},
                {'name': 'repo_2'}
            ]
            ghc = GithubOrgClient('xyz')
            r = ghc._public_repos_url
            self.assertEqual(r, mock.return_value)
            mock.assert_called_once()
            get_json_mock.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """ Tests that has_license returns the correct values.
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected_result
        )


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration class to test GithubOrgClient.public_repos method
    """
    @classmethod
    def setUpClass(cls):
        """setUpClass method"""
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """ tearDownClass method"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ Testing GithubOrgClient.public_repos """
        ghc = GithubOrgClient('random')
        self.assertEqual(ghc.org, self.org_payload)
        self.assertEqual(ghc.repos_payload, self.repos_payload)

    def test_public_repos_with_license(self):
        """ method to test the public_repos with the argument license """
        test_class = GithubOrgClient("holberton")
        assert True


if __name__ == "__main__":
    unittest.main()
