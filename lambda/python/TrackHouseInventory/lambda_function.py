import os
from datetime import datetime

import boto3
import requests
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    SITE = os.environ['site']
    field_map = fetch_fields(SITE)
    save_fields_to_db(field_map)


def fetch_fields(url: str):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    field_map = {}
    table = soup.find('table', attrs={'class': 'table--plain table-stats'})

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        field_map[cols[0].get_text().rstrip()] = cols[1].get_text()

    return field_map


def save_fields_to_db(fields: dict):
    date_string = datetime.today().strftime('%Y-%m-%d')
    dynamodb = boto3.client('dynamodb')
    for field in fields:
        print(f"PUT {date_string} = {field} = {fields[field]} ")
        result = dynamodb.put_item(TableName='HomeStats',
                                   Item={
                                       'Field': {'S': field},
                                       'Date': {'S': date_string},
                                       'Value': {'S': fields[field]}
                                   }
                                   )
        print(f"Result {result}")
