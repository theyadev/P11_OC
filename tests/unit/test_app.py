import pytest
from server import app as flask_app


@pytest.fixture()
def app():
    app = flask_app
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_request_example(client):
    response = client.get("/")
    assert b"<h1>Welcome to the GUDLFT Registration Portal!</h1>" in response.data


def test_show_summary(client):
    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"})

    assert b"Welcome, john@simplylift.co" in response.data


def test_show_summary_with_invalid_email(client):
    response = client.post(
        "/showSummary", data={"email": "test@gmail.com"})

    assert response.status_code == 404


def test_book(client):
    response = client.get("/book/Winter Festival/Simply Lift")

    assert response.status_code == 200
    assert b"Winter Festival" in response.data


def test_book_with_invalid_club(client):
    response = client.get("/book/Winter Festival/Invalid Club")

    assert b"Something went wrong-please try again" in response.data


def test_book_with_invalid_competition(client):
    response = client.get("/book/Invalid Competition/Simply Lift")

    assert b"Something went wrong-please try again" in response.data


def test_purchase_places(client):
    response = client.post(
        "/purchasePlaces", data={"club": "Simply Lift", "competition": "Winter Festival", "places": 5})

    assert response.status_code == 200


def test_purchase_places_with_invalid_club(client):
    response = client.post(
        "/purchasePlaces", data={"club": "invalid", "competition": "Winter Festival", "places": 5})

    assert b"Something went wrong-please try again" in response.data


def test_purchase_more_places(client):
    response = client.post(
        "/purchasePlaces", data={"club": "Simply Lift", "competition": "Winter Festival", "places": 9})

    assert b"Sorry, there are not enough places available" in response.data


def test_purchase_more_than_twelve_places(client):
    response = client.post(
        "/purchasePlaces", data={"club": "Simply Lift", "competition": "Fall Classic", "places": 13})

    assert b"You cannot book more than 12 places" in response.data


def test_purchase_negative_places(client):
    response = client.post(
        "/purchasePlaces", data={"club": "Simply Lift", "competition": "Winter Festival", "places": -1})

    assert b"You cannot book a negative number of places" in response.data


def test_purchase_more_than_we_have(client):
    response = client.post(
        "/purchasePlaces", data={"club": "Iron Temple", "competition": "Fall Classic", "places": 6})
    assert b"Sorry, you do not have enough points to book this number of places" in response.data


def test_purchase_expired_competition(client):
    response = client.post(
        "/purchasePlaces", data={"club": "Simply Lift", "competition": "Spring Festival", "places": 6})

    assert b"Sorry, you cannot book for a competition in the past" in response.data
