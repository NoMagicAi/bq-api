import re
#@TODO total refactor, YAML would be probably better for longer SQLs
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

PARAM_PLACEHOLDER = r"{% \S+ %}"

def get_query_by_slug(query_list, slug):
  for record in query_list["saved_queries"]:
    if "slug" in record and record["slug"] == slug:
      return record
  raise KeyError("Query not found")  # probably better exception exists

def contains_params(sql):
  return re.search(PARAM_PLACEHOLDER, sql)