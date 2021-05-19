import connexion
import six

from openapi_server.models.data_request_body import DataRequestBody  # noqa: E501
from openapi_server.models.query_result import QueryResult  # noqa: E501
from openapi_server.models.saved_query import SavedQuery  # noqa: E501
from openapi_server import util

from openapi_server.repositories.saved_query_repository import SAVED_QUERIES, get_query_by_slug, contains_params
from openapi_server.services.query_parser import QueryParser

def get_data(saved_query_slug):  # noqa: E501
    """Retrieve a single saved query result

    Retrieve a single saved query result - it works only for not parametrized queries # noqa: E501

    :param saved_query_slug: Slug of the saved query desired to be retrieved
    :type saved_query_slug: str

    :rtype: QueryResult
    """

    res = {}

    try:
      query = SavedQuery.from_dict(get_query_by_slug(SAVED_QUERIES, saved_query_slug))
    except KeyError:
      return {"error": "Query not found"}, 404

    sql = query.sql

    # if SQL query contains placeholder for values, replace them with provided values
    if contains_params(sql):
        return None, 406

    res['executed_sql'] = sql
    return QueryResult.from_dict(res)



def get_data_with_params(saved_query_slug, body=None):  # noqa: E501
    """Retrieve a single saved query result

    Retrieve a single saved query result # noqa: E501

    :param saved_query_slug: Slug of a saved query to be executed
    :type saved_query_slug: str
    :param body: values provided for mapametrized query
    :type body: dict | bytes

    :rtype: QueryResult
    """

    res = {}

    try:
      query = SavedQuery.from_dict(get_query_by_slug(SAVED_QUERIES, saved_query_slug))
    except KeyError:
      return {"error": "Query not found"}, 404

    sql = query.sql

    # if SQL query contains placeholder for values, replace them with provided values
    if connexion.request.is_json and contains_params(sql):
        body = DataRequestBody.from_dict(connexion.request.get_json())  # noqa: E501
        if not body.values:
            return None, 406
        sql = QueryParser.parse(query, body.values)

    res['executed_sql'] = sql
    return QueryResult.from_dict(res)

