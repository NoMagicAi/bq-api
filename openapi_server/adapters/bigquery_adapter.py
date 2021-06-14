from google.cloud import bigquery

DEFAULT_BQ_PROJECT = "staging-nomagic-ai"
LOCATION = "EU"
CLIENT = bigquery.Client(project=DEFAULT_BQ_PROJECT)

class BigqueryAdapter:
    @staticmethod
    def get_result_as_dict(sql: str) -> dict:
        query_job = CLIENT.query(sql, location=LOCATION).result()
        records = [dict(row) for row in query_job]

        return records