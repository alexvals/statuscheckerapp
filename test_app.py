from app import app, is_reachable, get_status_code, check_single_url
import pytest

#to run this file use: python -m pytest test_app.py -v

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_api_page(client):
    response = client.get('/api')
    assert response.status_code == 200

def test_google_ping():
    result = get_status_code("https://www.google.com")
    assert result == 200

@pytest.fixture
def client():
    client = app.test_client()
    return client

def test_bad_ping():
    result = get_status_code("https://notawebsitehaha")
    assert result == "UNREACHABLE"

def test_404_page():
    result = get_status_code("https://bbc.co.uk/404")
    assert result == 404

def test_bbc_sports_page():
    result = check_single_url("https://www.bbc.co.uk/sport")
    assert result == "200"

def test_is_reachable_google():
    result = is_reachable("www.google.com")
    assert result == True

def test_if_fake_website_works():
    result = is_reachable("sajdkjhsdkjhsd.dkfldfk")
    assert result == False
