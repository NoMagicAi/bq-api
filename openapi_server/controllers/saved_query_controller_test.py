# coding: utf-8

from __future__ import absolute_import
import unittest
import pytest

from flask import json
from six import BytesIO

from openapi_server.models.data_request_body import DataRequestBody  # noqa: E501
from openapi_server.models.query_result import QueryResult  # noqa: E501
from openapi_server.test import BaseTestCase

@pytest.mark.skip(reason="dont want to run integration tests now")
class TestQueryResultController(BaseTestCase):
    """QueryResultController integration test stubs"""

    def test_get_data(self):
        """Test case for get_data

        Retrieve a single saved query result
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/data/{saved_query_slug}'.format(saved_query_slug='saved_query_slug_example'),
            method='GET',
            headers=headers)
        # @TODO test 200 and 406
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_data_with_params(self):
        """Test case for get_data_with_params

        Retrieve a single saved query result
        """
        body = {
          "values" : [ {
            "name" : "evaluation_id",
            "value" : "7777"
          }, {
            "name" : "evaluation_id",
            "value" : "7777"
          } ]
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        # returns 404 when query not found by given slug
        # @TODO test 200 and 406
        response = self.client.open(
            '/v1/data/{saved_query_slug}'.format(saved_query_slug='saved_query_slug_example'),
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert404(response,
                       'Response body is: \n' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
