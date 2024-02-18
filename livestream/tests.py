import requests
import pytest
from django.test import TestCase

# Create your tests here.


pytestmark = pytest.mark.django_db


CHECK_LIVE_STATUS_URL = "http://localhost:8000/api/live/check-live-status/"


def test_check_live_status_endpoint_by_post():
    response = requests.post(CHECK_LIVE_STATUS_URL)
    assert response.status_code == 405


def test_check_live_status_valid_url_online():
    youtube_url = "https://www.youtube.com/live/jfKfPfyJRdk?si=bPiUUbV-k7iZt8g4"
    response = requests.get(CHECK_LIVE_STATUS_URL, params={"youtube_url": youtube_url})
    assert response.status_code == 200

    json_response = response.json()

    assert "title" in json_response
    assert "channel_name" in json_response
    assert "channel_id" in json_response
    assert "video_id" in json_response
    assert json_response["video_id"] == "jfKfPfyJRdk"
    assert "URL" in json_response
    assert "live_status" in json_response
    assert json_response["live_status"] == True


def test_check_live_status_valid_url_offline():
    youtube_url = "https://www.youtube.com/live/l-v8B4GnIWc?si=bYhc1DdF8aTuir7U"
    response = requests.get(CHECK_LIVE_STATUS_URL, params={"youtube_url": youtube_url})
    assert response.status_code == 200

    json_response = response.json()

    assert "title" in json_response
    assert "channel_name" in json_response
    assert "channel_id" in json_response
    assert "video_id" in json_response
    assert json_response["video_id"] == "l-v8B4GnIWc"
    assert "URL" in json_response
    assert "live_status" in json_response
    assert json_response["live_status"] == False


def test_check_live_status_empty_url():
    youtube_url = ""

    response = requests.get(CHECK_LIVE_STATUS_URL, params={"youtube_url": youtube_url})

    assert response.status_code == 400

    json_response = response.json()

    assert "detail" in json_response
    assert json_response["detail"] == "YouTube 網址不能為空。"


def test_check_live_status_inexistence_url():
    youtube_url = "123"

    response = requests.get(CHECK_LIVE_STATUS_URL, params={"youtube_url": youtube_url})

    assert response.status_code == 400

    json_response = response.json()

    assert "detail" in json_response
    assert json_response["detail"] == "YouTube 直播不存在。"
