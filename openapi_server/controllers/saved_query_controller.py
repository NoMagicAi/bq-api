import connexion
import six

from openapi_server.models.saved_queries_response import SavedQueriesResponse  # noqa: E501
from openapi_server.models.saved_query import SavedQuery  # noqa: E501
from openapi_server import util

SAVED_QUERIES = {
  "saved_queries": [
    {
      "slug": "kpi-competec-lab-all",
      "sql": "SELECT robot_name, evaluation_id, all_requests, injection_success_rate, soft_failure_rate hard_failure_rate FROM `staging-nomagic-ai.kpi_v2.kpi_competec` ORDER BY evaluation_id DESC LIMIT 100;"
    },
    {
      "slug": "kpi-competec-lab",
      "sql": "SELECT robot_name, evaluation_id, all_requests, injection_success_rate, soft_failure_rate hard_failure_rate FROM `staging-nomagic-ai.kpi_v2.kpi_competec` WHERE evaluation_id = {% evaluation_id %};",
      "params": [
          {
            "name": "evaluation_id",
            "type": "int"
          }
        ]
    }
  ]
}

def _get_query_by_slug(query_list, slug):
  for record in query_list["saved_queries"]:
    if "slug" in record and record["slug"] == slug:
      return record
  raise KeyError("Query not found")  # probably better exception exists


def get_saved_query_by_slug(saved_query_slug):  # noqa: E501
    """Retrieve a single saved query

    Retrieve a single saved query # noqa: E501

    :param saved_query_slug: Slug of the saved query desired to be retrieved
    :type saved_query_slug: str

    :rtype: SavedQuery
    """

    try:
      query = _get_query_by_slug(SAVED_QUERIES, saved_query_slug)
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
