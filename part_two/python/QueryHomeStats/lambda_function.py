import json

import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = "HomeStatsDB"


def lambda_handler(event, context_ignore_me):
    try:
        print(F"EVENT {event}")
        dynamodb = boto3.resource("dynamodb")

        if "queryStringParameters" not in event or event["queryStringParameters"] is None \
                or "field" not in event["queryStringParameters"]:
            return wrap_response(find_distinct_field_names(dynamodb))

        field = event["queryStringParameters"]["field"]
        return wrap_response(run_query_on_field(dynamodb, field))
    except Exception as e:
        return wrap_response(F"Error when trying to run query: {e}", status_code=500)


def wrap_response(response_body, status_code=200):
    print(response_body)
    response = {
        "statusCode": status_code,
        "headers": {},
        "body": response_body
    }
    return response


def find_distinct_field_names(dynamodb_resource):
    response = dynamodb_resource.Table(TABLE_NAME).scan()

    # we want to avoid duplicates
    fields_set = {i['Field'] for i in response['Items']}

    # convert set to list
    fields = list(fields_set)

    # sort the list so results are predictable
    fields.sort()

    return json.dumps(fields)


def run_query_on_field(dynamodb_resource, field):
    response = dynamodb_resource.Table(TABLE_NAME).query(
        KeyConditionExpression=Key('Field').eq(field)
    )


    response_body = "Date,Value\n"
    for record in response['Items']:
        date = record['Date']
        value = record['Value'].replace(',', '').replace('£', '').replace(' days', '')
        if value != "0":
            response_body += F"{date},{value}\n"

    return response_body
