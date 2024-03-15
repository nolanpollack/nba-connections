from service import handler

def test_handler():
    event = {
        "p1": "LeBron James",
        "p2": "Kareem Abdul-Jabbar"
    }
    response = handler(event, None)
    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    print(response["body"])

test_handler()