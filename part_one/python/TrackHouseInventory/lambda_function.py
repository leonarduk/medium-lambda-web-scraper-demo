import os
from datetime import datetime

import boto3
import requests
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    site = os.environ['site']
    field_map = fetch_fields(site)
    dynamodb = boto3.client('dynamodb')

    save_fields_to_db(field_map, dynamodb)


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


def save_fields_to_db(fields: dict, dynamodb):
    date_string = datetime.today().strftime('%Y-%m-%d')
    for field in fields:
        print(f"PUT {date_string} = {field} = {fields[field]} ")
        table = dynamodb.Table('HomeStatsDB')
        result = table.put_item(Item={
                                       'Field': field,
                                       'Date': date_string,
                                       'Value': fields[field]
                                   }
                                   )
        print(f"Result {result}")
