from service import handler

def test_handler():
    event = {
        "queryStringParameters": {
            "p1": "Lebron James",
            "p2": "Kyrie Irving"
        }
    }
    response = handler(event, None)
    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    print(response["body"])

test_handler()