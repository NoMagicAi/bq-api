import pytest
from openapi_server.services.query_parser import QueryParser
from openapi_server.models.saved_query import SavedQuery  # noqa: E501
from openapi_server.models.query_value import QueryValue  # noqa: E501


@pytest.fixture
def saved_query_no_params_fixture():
    fixture = {
          "sql": "SELECT 7 AS test;",
          "slug": "fixture"
    }
    return SavedQuery.from_dict(fixture)

@pytest.fixture
def saved_query_fixture():
    fixture = {
          "sql": "SELECT 7 AS test FROM attampts WHERE evaluation_id={% evaluation_id %};",
          "slug": "fixture",
          "params": [
            {
               "name": "evaluation_id",
               "type": "int"
            }
        ]
    }
    return SavedQuery.from_dict(fixture)

@pytest.fixture
def saved_query_fixture_2_params():
    fixture = {
          "sql": "SELECT 7 AS test FROM attampts WHERE evaluation_id={% evaluation_id %} AND robot_name={% robot_name %};",
          "slug": "fixture",
          "params": [
            {
               "name": "evaluation_id",
               "type": "int"
            },
            {
                "name": "robot_name",
                "type": "str"
            }
        ]
    }
    return SavedQuery.from_dict(fixture)

@pytest.fixture
def value_fixture():
    fixture = {
          "name": "evaluation_id",
          "value": "7000"
    }
    return QueryValue.from_dict(fixture)


@pytest.fixture
def two_values_fixture():
    val_1 = {
        "name": "evaluation_id",
        "value": "7000"
    }
    val_2 = {
        "name": "robot_name",
        "value": "Julia"
    }
    return [QueryValue.from_dict(val_1), QueryValue.from_dict(val_2)]


@pytest.fixture
def value_mismatch_fixture():
    fixture = {
          "name": "zupa",
          "value": "7000"
    }
    return QueryValue.from_dict(fixture)

def test_query_parser_no_params(saved_query_no_params_fixture):
    sql = QueryParser.parse(query=saved_query_no_params_fixture)
    assert sql == saved_query_no_params_fixture.sql

def test_query_parser_no_value(saved_query_fixture):
    """throws when no value provided for given parameter"""
    with pytest.raises(ValueError):
        QueryParser.parse(query=saved_query_fixture)

    with pytest.raises(ValueError):
        QueryParser.parse(query=saved_query_fixture, values=[])

    with pytest.raises(ValueError):
        QueryParser.parse(query=saved_query_fixture, values=[QueryValue.from_dict({})])

def test_query_parser_value_mismatch(saved_query_fixture, value_mismatch_fixture):
    """throws when no value provided for given parameter"""
    with pytest.raises(ValueError):
        QueryParser.parse(query=saved_query_fixture, values=[value_mismatch_fixture])

def test_query_parser_happy_path(saved_query_fixture, value_fixture):
    sql = QueryParser.parse(query=saved_query_fixture, values=[value_fixture])
    assert sql == "SELECT 7 AS test FROM attampts WHERE evaluation_id=7000;"


def test_query_parser_2_params_1_missed(saved_query_fixture_2_params, value_fixture):
    with pytest.raises(ValueError):
        QueryParser.parse(query=saved_query_fixture_2_params, values=[value_fixture])

def test_query_parser_1_redundant_value(saved_query_fixture, two_values_fixture):
    sql = QueryParser.parse(query=saved_query_fixture, values=two_values_fixture)
    assert sql == "SELECT 7 AS test FROM attampts WHERE evaluation_id=7000;"


def test_query_parser_happy_path_2_params(saved_query_fixture_2_params, two_values_fixture):
    sql = QueryParser.parse(query=saved_query_fixture_2_params, values=two_values_fixture)
    assert sql == "SELECT 7 AS test FROM attampts WHERE evaluation_id=7000 AND robot_name=\"Julia\";"
