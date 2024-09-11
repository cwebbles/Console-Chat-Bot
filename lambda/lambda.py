import boto3
import os
import json
from openai import OpenAI

def get_open_ai_secret():
    sm_client = boto3.client('secretsmanager')
    secret_name = os.getenv('OPEN_AI_SECRET_NAME')

    response = sm_client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    return secret['OPEN_AI']

def lambda_handler(event, context):

    open_ai_client = OpenAI()

    try:
        open_ai_client.api_key = get_open_ai_secret()

        completion = open_ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": event['message']
                }
            ]
        )

        return {
            'statusCode': 200,
            'body': {
                'response': completion.choices[0].text
            }
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'Internal Server Error'
        }

