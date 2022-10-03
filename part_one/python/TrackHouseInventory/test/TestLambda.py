import os
import os.path
import unittest
from datetime import datetime
from unittest import mock

import boto3  # AWS SDK for Python
from moto.dynamodb import mock_dynamodb  # since we're going to mock DynamoDB service

from ..lambda_function import save_fields_to_db, fetch_fields


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def text(self):
            return self.text

    if args[0] == 'https://www.home.co.uk/company/stats.htm':
        current_dir = os.path.dirname(__file__)

        with open(os.path.join(current_dir, 'Home.co.ukWebsiteStatistics.htm'), 'r') as file:
            data = file.read().rstrip()
        return MockResponse(data, 200)

    return MockResponse(None, 404)


def create_stats_table(db):
    table = db.create_table(
        TableName='HomeStatsDB',
        KeySchema=[
            {
                'AttributeName': 'Field',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'Date',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Field',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Date',
                'AttributeType': 'S'
            }],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='HomeStatsDB')
    assert table.table_status == 'ACTIVE'

    return table


@mock_dynamodb
class TestLambda(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_fetch_fields(self, mock_get):
        """
        If you want this test to read from the internet and not this local file,
        then remove

            @mock.patch('requests.get', side_effect=mocked_requests_get)

        and change the signature to:

            def test_fetch_fields(self):
        """
        values = fetch_fields(url='https://www.home.co.uk/company/stats.htm')
        assert len(values.values()) == 11

    def test_save_fields_to_db(self):
        """
        Create database resource and mock table
        """
        db = boto3.resource('dynamodb')

        table = create_stats_table(db=db)

        fields = {"field1": "value1", "field2": "value2"}
        save_fields_to_db(fields=fields, dynamodb=db)

        date_string = datetime.today().strftime('%Y-%m-%d')

        response = table.get_item(Key={'Field': "field1", "Date": date_string})
        assert response['Item']['Field'] == "field1"
        assert response['Item']['Date'] == date_string
        assert response['Item']['Value'] == "value1"


if __name__ == '__main__':
    unittest.main()
