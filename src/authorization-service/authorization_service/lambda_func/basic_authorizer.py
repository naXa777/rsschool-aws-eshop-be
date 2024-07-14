import os
import base64
import traceback

def handler(event, context):
    print("auth request")

    auth_header = event["authorizationToken"]

    try:
        scheme, encoded_creds = auth_header.split(' ')
        decoded_creds = base64.b64decode(encoded_creds).decode('utf-8')
        username, password = decoded_creds.split(':')
        stored_password = os.getenv(username)

        print(f'scheme {scheme} username {username}')

        if scheme == 'Basic' and stored_password and stored_password == password:
            policy = generatePolicy(username, 'Allow', event['methodArn'])
            print(f'policy {policy}')
            return policy
        else:
            policy = generatePolicy(username, 'Deny', event['methodArn'])
            print(f'policy {policy}')
            return policy
    except Exception:
        return generatePolicy('unknown', 'Deny', event['methodArn'])

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
