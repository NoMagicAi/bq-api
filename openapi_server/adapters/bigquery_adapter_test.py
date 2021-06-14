import pytest

# https://stackoverflow.com/questions/57808461/how-to-mock-a-google-api-library-with-python-3-7-for-unit-testing
# https://stackoverflow.com/questions/53700181/python-unit-testing-google-bigquery
#
# from google.cloud import bigquery
#
#
# schema = [
#     bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
# ]
#
#
# def some_query(table_name='blahblahbloo'):
#
#     client = bigquery.Client()
#     table_id = f"project.dataset.{table_name}"
#     table = bigquery.Table(table_id, schema=schema)
#     table = client.create_table(table)
#
#
# def test_some_query(mocker):
#     mock_table = mocker.patch('google.cloud.bigquery.Table', autospec=True)
#     mock_client = mocker.patch('google.cloud.bigquery.Client', autospec=True)
#
#     some_query()  # run with mocked objects
#
#     mock_table.assert_called_with('project.dataset.blahblahbloo', schema=schema)
#     mock_client().create_table.assert_called_with(mock_table.return_value)

# https://pypi.org/project/bq-test-kit/
