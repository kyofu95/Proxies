from flask import Flask


def test_api(setup_flask: Flask):
    with setup_flask.test_client() as client:
        response = client.get("/api/proxies")

        assert response.status_code == 200
        assert len(response.json) == 3

        json = response.json
        assert json[0]["address"] == "30.0.0.1"
        assert json[1]["address"] == "30.0.0.2"
        assert json[2]["address"] == "30.0.0.3"


def test_api_country(setup_flask: Flask):
    with setup_flask.test_client() as client:
        data = {
            "country": "Japan"
        }
        response = client.get("/api/proxies", query_string=data)

        assert response.status_code == 200
        assert len(response.json) == 1

        json = response.json
        assert json[0]["address"] == "30.0.0.3"
        assert json[0]["country"] == "Japan"

def test_api_protocol(setup_flask: Flask):
    with setup_flask.test_client() as client:
        data = {
            "protocol": "SOCKS4"
        }
        response = client.get("/api/proxies", query_string=data)

        assert response.status_code == 200
        assert len(response.json) == 2

        json = response.json
        assert json[0]["protocol"] == "SOCKS4"
        assert json[1]["protocol"] == "SOCKS4"
