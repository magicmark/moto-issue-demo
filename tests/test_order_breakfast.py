import unittest
import pytest
import boto3
import moto
from moto_issue_demo.order_breakfast import main as order_breakfast

@pytest.fixture(autouse=True, scope="function")
def dynamodb():
    with moto.mock_dynamodb():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        dynamodb.create_table(
            TableName="meal-orders",
            KeySchema=[
                {"AttributeName": "customer", "KeyType": "HASH"},
                {"AttributeName": "mealtime", "KeyType": "SORT"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "customer", "AttributeType": "S"},
                {"AttributeName": "mealtime", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        yield dynamodb


def test_breakfast_order(dynamodb):
    dynamodb.Table("meal-orders").put_item(
        Item={
            "customer": "mark",
            "mealtime": "breakfast",
            "lock": {
                "acquired_at": 123
            }
        }
    )

    try:
        order_breakfast()
    except BaseException as err:
        assert 'Item' in err.response["CancellationReasons"][0]