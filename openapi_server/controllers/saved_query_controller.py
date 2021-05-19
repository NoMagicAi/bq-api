import connexion
import six

from openapi_server.models.saved_queries_response import SavedQueriesResponse  # noqa: E501
from openapi_server.models.saved_query import SavedQuery  # noqa: E501
from openapi_server import util

from openapi_server.repositories.saved_query_repository import SAVED_QUERIES, get_query_by_slug


def get_saved_query_by_slug(saved_query_slug):  # noqa: E501
    """Retrieve a single saved query

    Retrieve a single saved query # noqa: E501

    :param saved_query_slug: Slug of the saved query desired to be retrieved
    :type saved_query_slug: str

    :rtype: SavedQuery
    """

    try:
      query = get_query_by_slug(SAVED_QUERIES, saved_query_slug)
    except KeyError:
      return {"error": "Query not found"}, 404

    # return query
    return SavedQuery.from_dict(query) 

def list_saved_queries():  # noqa: E501
    """Retrieves the list of all saved queries

    Retrieves the list of all saved queries # noqa: E501


    :rtype: SavedQueriesResponse
    """
    return SAVED_QUERIES
