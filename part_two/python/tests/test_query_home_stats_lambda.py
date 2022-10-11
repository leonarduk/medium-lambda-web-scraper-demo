from datetime import datetime
import unittest

import boto3  # AWS SDK for Python
from moto.dynamodb import mock_dynamodb  # since we're going to mock DynamoDB service

from part_two.python.tests.mock_db_utils import create_stats_table
from part_two.python.QueryHomeStats.lambda_function import find_distinct_field_names, run_query_on_field, lambda_handler
from part_two.python.TrackHouseInventory.lambda_function import save_fields_to_db

@mock_dynamodb
class TestLambda(unittest.TestCase):

    def test_find_distinct_field_names(self):
        # Create a mock database table
        db = boto3.resource('dynamodb')
        create_stats_table(db=db)

        # populate it with two fields
        fields = {"field1": "value1", "field2": "value2"}
        save_fields_to_db(fields=fields, dynamodb=db)

        # run the code under test
        actual = find_distinct_field_names()
        expected = '["field1", "field2"]'
        assert actual == expected

    def test_run_query_on_field(self):
        # Create a mock database table
        db = boto3.resource('dynamodb')
        create_stats_table(db=db)

        # populate it with two fields
        fields = {"field1": "value1", "field2": "value2"}
        save_fields_to_db(fields=fields, dynamodb=db)

        # run the code under test
        actual = run_query_on_field(dynamodb_resource=db, field="field1")
        print(actual)

        date_string = datetime.today().strftime('%Y-%m-%d')

        # verify results as expected
        assert actual == f"""Date,Value
{date_string},value1
"""

    def test_lambda_handler_fail(self):
        event = []
        actual = lambda_handler(event=event, context_ignore_me=None)
        print(actual)
        assert actual.get("statusCode") == 500

    def test_lambda_handler_return_fields(self):
        # Create a mock database table
        db = boto3.resource('dynamodb')
        create_stats_table(db=db)

        # populate it with two fields
        fields = {"field1": "value1", "field2": "value2"}
        save_fields_to_db(fields=fields, dynamodb=db)

        event = []
        actual = lambda_handler(event=event, context_ignore_me=None)
        print(actual)
        assert actual.get("statusCode") == 200
        assert actual.get("body") == '["field1", "field2"]'

    def test_lambda_handler_return_fields(self):
        # Create a mock database table
        db = boto3.resource('dynamodb')
        create_stats_table(db=db)

        # populate it with two fields
        fields = {"field1": "value1", "field2": "value2"}
        save_fields_to_db(fields=fields, dynamodb=db)

        event = {"queryStringParameters": {"field": "field1"}}
        actual = lambda_handler(event=event, context_ignore_me=None)
        print(actual)
        assert actual.get("statusCode") == 200
        assert actual.get("body") == 'Date,Value\n2022-10-11,value1\n'


if __name__ == '__main__':
    unittest.main()
