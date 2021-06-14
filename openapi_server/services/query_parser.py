import re
from typing import List
from openapi_server.models.saved_query import SavedQuery  # noqa: E501
from openapi_server.models.query_value import QueryValue  # noqa: E501
from openapi_server.models.query_params import QueryParams  # noqa: E501


QueryValues = List[QueryValue]

class QueryParser:
    @staticmethod
    def parse(query: SavedQuery, values: QueryValues = []) -> str:
        """Returns a SQL query with all values inserted instead of placeholders"""
        sql = query.sql
        if not query.params:
            return sql
        for param in query.params:
            if not values:
                raise ValueError("For each param value must be provided. No values given.")
            mismatched = QueryParser._mismatched(query.params, values)
            if mismatched:
                raise ValueError(
                    f"For each param value must be provided. Mismatched params: {mismatched}. Expected params list: {query.params}. Values provided: {values}")
            for value in values:
                if value.name == param.name:
                    sql = QueryParser._replace(sql=sql, param_type=param.type, name=value.name, value=value.value)
        return sql

    @staticmethod
    def _mismatched(query_params: QueryParams = [], values: QueryValues = []) -> QueryParams:
        required = {o.name for o in query_params}
        given = {o.name for o in values}

        return required.difference(given)

    @staticmethod
    def _replace(sql: str, param_type: str, name: str, value: str) -> str:
        if param_type == 'int':
            sql = sql.replace("{% " + f"{name}" + " %}", str(value))

        elif param_type == 'str':
            sql = sql.replace("{% " + f"{name}" + " %}", f'"{value}"')
        else:
            raise ValueError(f"This type is not allowed: {param_type}")

        return sql
