import json

import boto3

# https://www.fernandomc.com/posts/ten-examples-of-getting-data-from-dynamodb-with-python-and-boto3/

TABLE_NAME = "HomeStats"


def lambda_handler(event, context):
    print(F"EVENT {event}")
    dynamodb_client = boto3.client("dynamodb")

    if "queryStringParameters" not in event or event["queryStringParameters"] is None \
            or "field" not in event["queryStringParameters"]:
        return wrap_response(find_distinct_field_names())

    field = event["queryStringParameters"]["field"]
    return wrap_response(run_query_on_field(dynamodb_client, field))


def wrap_response(response_body):
    print(response_body)
    response = {
        "statusCode": 200,
        "headers": {},
        "body": response_body
    }
    return response


def find_distinct_field_names():
    response = boto3.resource(
        'dynamodb').Table(TABLE_NAME).scan()
    fields_set = {i['Field'] for i in response['Items']}
    return json.dumps(list(fields_set))


def run_query_on_field(dynamodb_client, field):
    response = dynamodb_client.query(
        TableName=TABLE_NAME,
        KeyConditionExpression='Field = :field',
        ExpressionAttributeValues={
            ':field': {'S': field}
        }
    )
    response_body = "Date,Value\n"
    for record in response['Items']:
        date = record['Date']['S']
        value = record['Value']['S'].replace(',', '').replace('£', '').replace(' days', '')
        if value != "0":
            response_body += F"{date},{value}\n"

    return response_body
