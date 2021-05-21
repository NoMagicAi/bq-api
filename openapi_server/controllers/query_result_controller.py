import connexion
import six

from openapi_server.models.query_result import QueryResult  # noqa: E501
from openapi_server.repositories.saved_query_repository import SAVED_QUERIES, get_query_by_slug, get_res


def get_data(saved_query_slug):  # noqa: E501
    """Retrieve a single saved query result

    Retrieve a single saved query result - it works only for not parametrized queries # noqa: E501

    :param saved_query_slug: Slug of the saved query desired to be retrieved
    :type saved_query_slug: str

    :rtype: QueryResult
    """
    try:
        query = get_query_by_slug(SAVED_QUERIES, saved_query_slug)
    except KeyError:
        return {"error": "Query not found"}, 404

    # if SQL query contains placeholder for values, replace them with provided values
    # for GET - it will throw 406 if any values needed (SQL contains placeholders)
    # in such case you should use POST
    request_json = connexion.request.get_json() if connexion.request.is_json else None
    try:
        res = get_res(request_json, query)
    except ValueError as e:
        return {"error": "Values for parametrized query not provided", "payload": e.args}, 406

    # data from DB wasn't correctly processed here, maybe contract is somehow wrong
    # return QueryResult.from_dict(res)
    return res

# @TODO body should be used?
# @TODO maybe there should be one method for both POST and GET here, code is the same
def get_data_with_params(saved_query_slug, body=None):  # noqa: E501
    """Retrieve a single saved query result

    Retrieve a single saved query result # noqa: E501

    :param saved_query_slug: Slug of a saved query to be executed
    :type saved_query_slug: str
    :param body: values provided for mapametrized query
    :type body: dict | bytes

    :rtype: QueryResult
    """
    try:
        query = get_query_by_slug(SAVED_QUERIES, saved_query_slug)
    except KeyError:
        return {"error": "Query not found"}, 404

    # if SQL query contains placeholder for values, replace them with provided values
    request_json = connexion.request.get_json() if connexion.request.is_json else None
    try:
        res = get_res(request_json, query)
    except ValueError:
        return {"error": "Values for parametrized query not provided"}, 406

    # data from DB wasn't correctly processed here, maybe contract is somehow wrong
    # return QueryResult.from_dict(res)
    return res
