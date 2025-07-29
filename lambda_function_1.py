import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('urlShortener')

def lambda_handler(event, context):
    try:
        short_code = event['pathParameters']['shortcode']
        response = table.get_item(Key={'shortCode': short_code})
        item = response.get('Item')

        if item:
            table.update_item(
                Key={'shortCode': short_code},
                UpdateExpression='ADD clicks :val',
                ExpressionAttributeValues={':val': 1}
            )

            return {
                'statusCode': 301,
                'headers': {'Location': item['originalURL']},
                'body': ''
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Short URL not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

