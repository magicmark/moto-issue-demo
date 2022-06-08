import boto3

def main():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

    dynamodb.meta.client.transact_write_items(
        TransactItems=[
            {
                "Update": {
                    "TableName": "meal-orders",
                    "Key": {"customer": "mark", "mealtime": "breakfast"},
                    # only let the customer place one order per meal at a time.
                    "UpdateExpression": "set #lock = :lock",
                    "ExpressionAttributeNames": {
                        "#lock": "lock",
                        "#acquired_at": "acquired_at",
                    },
                    "ExpressionAttributeValues": {":lock": { 'acquired_at': 123 }},
                    "ReturnValuesOnConditionCheckFailure": "ALL_OLD",
                    "ConditionExpression": "attribute_not_exists(#lock.#acquired_at)",
                }
            }
        ]
    )

