from flask import Flask

def test_index_page(setup_flask: Flask):
    with setup_flask.test_client() as client:
        response = client.get("/")

        assert response.status_code == 200
