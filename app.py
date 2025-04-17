"""Flask App Start Module."""
import os
import json
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from post_normalizer import PostNormalizer
from markupsafe import escape

# Create and name Flask app
app = Flask(__name__)
app.debug = os.environ.get('DEBUG', False)

# Setup CORS
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config['JSON_SORT_KEYS'] = False

# Configure logger
logger = logging.getLogger("FlaskAppLogger")
logger.setLevel(logging.DEBUG)

# Create console handler and set level to DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create formatter and add it to the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

# Supported platforms
SUPPORTED_PLATFORMS = ["Telegram", "Twitter", "Tiktok"]

# Helper Functions
def load_platform_mappings():
    """
    Load platform mappings from the JSON configuration file.

    Returns:
        dict: Platform mappings.
    """
    try:
        with open('./data/platform_mappings.json', 'r', encoding='utf-8') as config_file:
            platform_configs = json.load(config_file)
        logger.debug("Loaded platform mappings successfully.")
        return platform_configs
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise

def validate_platform(platform):
    """
    Validate if the platform is supported.

    Args:
        platform (str): The platform name to validate.

    Raises:
        ValueError: If the platform is not supported.
    """
    if platform not in SUPPORTED_PLATFORMS:
        logger.error(f"Invalid platform name: {platform}")
        raise ValueError("Invalid platform name")

def get_normalized_posts(platform):
    """
    Get normalized posts for a specific platform.

    Args:
        platform (str): The platform name.

    Returns:
        list: List of normalized posts.
    """
    platform_configs = load_platform_mappings()
    config = platform_configs.get(platform)
    if not config:
        logger.error(f"No configuration found for platform: {platform}")
        raise ValueError("Invalid platform configuration")

    logger.debug(f"Configuration for {platform}: {config}")
    normalizer = PostNormalizer(config["file_path"], config["mapping"])
    return normalizer.normalize()

# Error Handlers 500
@app.errorhandler(500)
def not_found_error(error):
    """
    Custom handler for 500 errors.

    Args:
        error: The error object.

    Returns:
        JSON: JSON response with error message.
    """
    logger.warning(f"500 error: {error}")
    return jsonify({"error": "The requested resource was not found"}), 500

# Error Handlers 404
@app.errorhandler(404)
def not_found_error(error):
    """
    Custom handler for 404 errors.

    Args:
        error: The error object.

    Returns:
        JSON: JSON response with error message.
    """
    logger.warning(f"404 error: {error}")
    return jsonify({"error": "The requested resource was not found"}), 404

# API Endpoints
@app.route("/", methods=["GET"])
def profile_list():
    """
    App route to list all posts for all platforms.

    Returns:
        JSON: JSON response containing the list of normalized posts.
    """
    logger.info("Processing request to list all posts.")
    try:
        platform_configs = load_platform_mappings()
        all_posts = []
        for platform in platform_configs.keys():
            logger.info(f"Processing data for platform: {platform}")
            all_posts.extend(get_normalized_posts(platform))
        return jsonify(all_posts)
    except FileNotFoundError:
        return jsonify({"error": "Configuration file not found"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in configuration file"}), 500
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route("/<platform>", methods=["GET"])
def post_by_platform(platform):
    """
    App route to list posts by platform.

    Args:
        platform (str): The platform name to filter posts.

    Returns:
        JSON: JSON response containing the list of normalized posts by platform.
    """
    # Escape the platform input to prevent XSS
    platform = escape(platform)
    logger.info(f"Processing request to list posts for platform: {platform}")
    try:
        # Validate the platform name
        validate_platform(platform)
        normalized_posts = get_normalized_posts(platform)
        return jsonify(normalized_posts)
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except FileNotFoundError:
        logger.error("Configuration file not found")
        return jsonify({"error": "Configuration file not found"}), 500
    except json.JSONDecodeError:
        logger.error("Invalid JSON format in configuration file")
        return jsonify({"error": "Invalid JSON format in configuration file"}), 500
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)