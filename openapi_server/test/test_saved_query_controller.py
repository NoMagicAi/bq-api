# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.saved_queries_response import SavedQueriesResponse  # noqa: E501
from openapi_server.models.saved_query import SavedQuery  # noqa: E501
from openapi_server.test import BaseTestCase


class TestSavedQueryController(BaseTestCase):
    """SavedQueryController integration test stubs"""

    def test_get_saved_query_by_slug(self):
        """Test case for get_saved_query_by_slug

        Retrieve a single saved query
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/saved_queries/{saved_query_slug}'.format(saved_query_slug='saved_query_slug_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_saved_queries(self):
        """Test case for list_saved_queries

        Retrieves the list of all saved queries
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/saved_queries',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
