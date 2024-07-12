import os
import base64
import traceback

def handler(event, context):
    print("auth request")

    auth_header = event["authorizationToken"]

    if not auth_header:
        return {
            'statusCode': 401,
            'body': 'Unauthorized'
        }

    encoded_creds = auth_header.split(' ')[1]
    decoded_creds = base64.b64decode(encoded_creds).decode('utf-8')
    username, password = decoded_creds.split('=')
    password = password.strip()

    stored_password = os.getenv(username)

    if stored_password and stored_password == password:
        return generatePolicy(username, 'Allow', event['methodArn'])
    else:
        return {
            'statusCode': 403,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "content-type": "application/json"
            },
            'body': 'Forbidden'
        }

def generatePolicy(principalId, effect, resource):
    authResponse = {
        'principalId': principalId
    }
    if effect and resource:
        policyDoc = {
            'Version': '2012-10-17',
            'Statement': []
        }
        statementOne = {
            'Action': 'execute-api:Invoke',
            'Effect': effect,
            'Resource': resource
        }
        policyDoc['Statement'] = [statementOne]
        authResponse['policyDocument'] = policyDoc

    return authResponse
