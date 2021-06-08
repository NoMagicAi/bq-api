import re

from openapi_server.models.saved_query import SavedQuery  # noqa: E501
from openapi_server.models.data_request_body import DataRequestBody  # noqa: E501
from openapi_server.services.query_parser import QueryParser
from openapi_server.adapters.bigquery_adapter import BigqueryAdapter

#@TODO total refactor, YAML would be probably better for longer SQLs
#@TODO probably I will remove project and dataset, so only staging:api would be available

# please DON'T specify a project, API connects to STAGING project ("staging-nomagic-ai")
# if you need e.g. data from PROD you can access it via VIEW in staging-nomagic-ai:api dataset
# @TODO easy to test in BQ console
SAVED_QUERIES = {
  "saved_queries": [
    {
      "slug": "kpi-competec-lab-all",
      "sql": "SELECT robot_name, evaluation_id, all_requests, injection_success_rate, soft_failure_rate, hard_failure_rate FROM `staging-nomagic-ai.kpi_v2.kpi_competec` ORDER BY evaluation_id DESC LIMIT 100;"
    },
    {
      "slug": "kpi-competec-lab",
      "sql": "SELECT robot_name, evaluation_id, all_requests, injection_success_rate, soft_failure_rate, hard_failure_rate FROM `staging-nomagic-ai.kpi_v2.kpi_competec` WHERE evaluation_id = {% evaluation_id %};",
      "params": [
          {
            "name": "evaluation_id",
            "type": "int"
          }
        ]
    }
  ]
}

PARAM_PLACEHOLDER = r"{% \S+ %}"

def get_query_by_slug(query_list, slug: str) -> SavedQuery:
  for record in query_list["saved_queries"]:
    if "slug" in record and record["slug"] == slug:
      return SavedQuery.from_dict(record)
  raise KeyError("Query not found")  # probably better exception exists

def _contains_params(sql):
  return re.search(PARAM_PLACEHOLDER, sql)

def get_res(request_json, query: SavedQuery) -> QueryParser:
  res = {}
  sql = query.sql
  res['sql'] = sql

  # if SQL query contains placeholder for values, replace them with provided values
  values = {}
  if request_json and _contains_params(sql):
    body = DataRequestBody.from_dict(request_json)  # noqa: E501
    if not body.values:
      raise ValueError("Values for parametrized query not provided", res)
    values = body.values

  res['executed_sql'] = QueryParser.parse(query, values)
  res['data'] = BigqueryAdapter.get_result_as_dict(res['executed_sql'])

  return res


