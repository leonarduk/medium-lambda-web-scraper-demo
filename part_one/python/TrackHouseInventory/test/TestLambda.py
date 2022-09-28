import unittest

import boto3  # AWS SDK for Python
from moto.dynamodb import mock_dynamodb  # since we're going to mock DynamoDB service

from ..lambda_function import save_fields_to_db, fetch_fields

from datetime import datetime


@mock_dynamodb
class TestLambda(unittest.TestCase):

    def test_fetch_fields(self):
        """
        This is actually an integration test, not a unit test as it goes to the internet to get that
        :return:
        """
        values = fetch_fields(url="https://www.home.co.uk/company/stats.htm")
        assert len(values.values()) == 11

    def test_save_fields_to_db(self):
        """
        Create database resource and mock table
        """
        db = boto3.resource('dynamodb')

        table = self.create_stats_table(db=db)

        fields = {"field1": "value1", "field2": "value2"}
        save_fields_to_db(fields=fields, dynamodb=db)

        date_string = datetime.today().strftime('%Y-%m-%d')

        response = table.get_item(Key={'Field': "field1", "Date": date_string})
        assert response['Item']['Field'] == "field1"
        assert response['Item']['Date'] == date_string
        assert response['Item']['Value'] == "value1"


    def create_stats_table(self, db):
        table = db.create_table(
            TableName='HomeStats',
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
        table.meta.client.get_waiter('table_exists').wait(TableName='HomeStats')
        assert table.table_status == 'ACTIVE'

        return table


if __name__ == '__main__':
    unittest.main()
