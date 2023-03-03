#!/usr/bin/env python3
"""
Module test_client
"""
import unittest
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock
from fixtures import TEST_PAYLOAD
from urllib.error import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """test for client.GithubOrgClient"""

    @parameterized.expand([
        ("google"),
        ("abc")
        ])
    @patch('client.get_json', return_value={"payload": True})
    def test_org(self, org_name, mock):
        """test org returns correct value"""
        test_class = GithubOrgClient(org_name)
        value = test_class.org

        self.assertEqual(value, mock.return_value)

        mock.assert_called_once()

    @parameterized.expand([
        ("django", {"repos_url": "django"})
        ])
    def test_public_repos_url(self, name, expected):
        """GithubOrgClient._public_repos_url"""
        with patch.object(GithubOrgClient,
                          "org",
                          new_callable=PropertyMock,
                          return_value=expected
                          ) as mock:
            test_class = GithubOrgClient(name)
            return_value = test_class._public_repos_url

            self.assertEqual(return_value,
                             mock.return_value.get('repos_url'))
            mock.assert_called_once()

    @patch('client.get_json', return_value=[{"name": 'react'}])
    def test_public_repos(self, mock_get_json):
        """test test_public_repos()
        in GithubOrgClient
        """
        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock,
                          return_value='https://api.github.com/'
                          ) as mock_rep:
            test_class = GithubOrgClient('react')
            return_value = test_class.public_repos()

            self.assertEqual(return_value, ['react'])
            mock_get_json.assert_called_once()
            mock_rep.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "react2"}}, "react", False),
        ({"license": {"key": "django"}}, "django", True)
        ])
    def test_has_license(self, repo, license, expected):
        """test  TestGithubOrgClient.test_has_license"""
        test_class = GithubOrgClient('django')
        return_value = test_class.has_license(repo, license)
        self.assertEqual(return_value, expected)


@parameterized_class(
        ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
        TEST_PAYLOAD
        )
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """setup class"""
        cls.get_patcher = patch('requests.get', side_effect=HTTPError)

    @parameterized.expand([
        ({"license": {"key": "react2"}}, "react", False),
        ({"license": {"key": "django"}}, "django", True)
        ])
    def test_has_license(self, repo, license, expected):
        """ test  TestGithubOrgClient.test_has_license"""
        test_class = GithubOrgClient('django')
        return_value = test_class.has_license(repo, license)
        self.assertEqual(return_value, expected)

    @classmethod
    def tearDownClass(cls):
        """teardown class"""
        cls.get_patcher.stop()

