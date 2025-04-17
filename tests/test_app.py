import os, sys
import json
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
import json
from unittest.mock import patch, mock_open
from app import app

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Mock data for platform_mappings.json
mock_platform_mappings = {
    "Telegram": {
        "file_path": "./data/telegram.json",
        "mapping": {
            "text": "tel_text",
            "summary": "tel_text_summary",
            "translated_text": "tel_text_translation",
            "media_url": "media_url"
        }
    }
}

# Mock data for normalized posts
mock_normalized_posts = [
    {
        "text": "Sample text",
        "summary": "Sample summary",
        "translated_text": "Translated text",
        "media_url": "https://example.com/media.jpg"
    }
]

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_platform_mappings))
@patch("app.PostNormalizer")
def test_profile_list(mock_post_normalizer, mock_open_file, client):
    """Test the '/' endpoint for listing all posts."""
    # Mock the normalize method
    mock_post_normalizer.return_value.normalize.return_value = mock_normalized_posts

    # Send GET request to the '/' endpoint
    response = client.get("/")

    # Assert the response
    assert response.status_code == 200
    assert response.json == mock_normalized_posts

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_platform_mappings))
@patch("app.PostNormalizer")
def test_post_by_platform_valid(mock_post_normalizer, mock_open_file, client):
    """Test the '/<platform>' endpoint for a valid platform."""
    # Mock the normalize method
    mock_post_normalizer.return_value.normalize.return_value = mock_normalized_posts

    # Send GET request to the '/Telegram' endpoint
    response = client.get("/Telegram")

    # Assert the response
    assert response.status_code == 200
    assert response.json == mock_normalized_posts

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_platform_mappings))
def test_post_by_platform_invalid_platform(mock_open_file, client):
    """Test the '/<platform>' endpoint with an invalid platform."""
    # Send GET request to an invalid platform
    response = client.get("/InvalidPlatform")

    # Assert the response
    assert response.status_code == 400
    assert response.json == {"error": "Invalid platform name"}

@patch("builtins.open", side_effect=FileNotFoundError)
def test_profile_list_file_not_found(mock_open_file, client):
    """Test the '/' endpoint when the configuration file is missing."""
    # Send GET request to the '/' endpoint
    response = client.get("/")

    # Assert the response
    assert response.status_code == 500
    assert response.json == {"error": "Configuration file not found"}

@patch("builtins.open", new_callable=mock_open, read_data="Invalid JSON")
def test_profile_list_invalid_json(mock_open_file, client):
    """Test the '/' endpoint when the configuration file contains invalid JSON."""
    # Send GET request to the '/' endpoint
    response = client.get("/")

    # Assert the response
    assert response.status_code == 500
    assert response.json == {"error": "Invalid JSON format in configuration file"}

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_platform_mappings))
@patch("app.PostNormalizer")
def test_post_by_platform_unexpected_error(mock_post_normalizer, mock_open_file, client):
    """Test the '/<platform>' endpoint for an unexpected error."""
    # Mock the normalize method to raise an exception
    mock_post_normalizer.return_value.normalize.side_effect = Exception("Unexpected error")

    # Send GET request to the '/Telegram' endpoint
    response = client.get("/Telegram")

    # Assert the response
    assert response.status_code == 500
    assert response.json == {"error": "An unexpected error occurred"}