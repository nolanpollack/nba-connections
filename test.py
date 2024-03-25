from service import handler


def test_handler():
    event = {
        "queryStringParameters": {
            "p1": "Victor+Wembanyama",
            "p2": "Al+Brightman"
        }
    }
    response = handler(event, None)
    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    print(response["body"])


test_handler()
