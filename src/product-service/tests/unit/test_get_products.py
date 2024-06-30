import json
import sys
import os
import pytest

lambda_dir = os.path.dirname('../../product_service/lambda_func')
sys.path.append(lambda_dir)
from product_service.lambda_func import product_list


@pytest.mark.skip(reason="Skipping this test as I'm not ready to mock DynamoDB")
def test_handler_returns_products():
    response = product_list.handler(None, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body[0]['id'] == '1'
    assert body[0]['title'] == 'Coffee Mug "DevOps"'
    assert body[0]['price'] == 15
    assert len(body) >= 3


if __name__ == '__main__':
    pytest.main()
