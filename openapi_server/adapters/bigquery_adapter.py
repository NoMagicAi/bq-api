from google.cloud import bigquery

DEFAULT_BQ_PROJECT = "staging-nomagic-ai"
LOCATION = "EU"
CLIENT = bigquery.Client(project=DEFAULT_BQ_PROJECT)

class BigqueryAdapter:
    @staticmethod
    def get_result_as_dict(sql: str) -> dict:
        query_job = BigqueryAdapter._query(sql)
        return BigqueryAdapter._to_dict(query_job)

    @staticmethod
    def _query(sql:str):
        #@TODO result typing
        query_job = CLIENT.query(sql, location=LOCATION).result()
        return query_job

    @staticmethod
    def _to_dict(query_job):
        # @TODO typing
        result = {}
        for row in query_job:
            idx = 0
            for key, value in row.items():
                if key not in result:
                    result[key] = {}
                result[key][idx] = value
                idx = idx + 1

        return result