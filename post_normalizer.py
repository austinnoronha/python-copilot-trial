"""
PostNormalizer Class:

Handles loading and normalizing data from platform-specific JSON files.
The normalize_telegram_data method maps Telegram-specific keys to the common structure.
Common Structure:

text: Original text of the post.
summary: Summary of the post.
translated_text: Translated version of the text (if available).
media_url: URL of any associated media.
Extensibility:

To support other platforms, add methods like normalize_<platform>_data and extend the normalize method to handle them.
Usage:

Replace file_path with the path to the desired platform's JSON file.
Run the script to see the normalized output.
"""

import json, os

class PostNormalizer:
    """A class to normalize post data from different platforms into a common structure."""

    def __init__(self, file_path, mapping):
        """
        Initialize the PostNormalizer with the path to the platform's JSON file and mapping.
        
        Args:
            file_path (str): Path to the JSON file containing platform-specific data.
            mapping (dict): A dictionary defining the mapping of platform-specific keys to common keys.
        """
        self.file_path = file_path
        self.mapping = mapping

    def load_data(self):
        """
        Load JSON data from the specified file path.
        
        Returns:
            list: A list of dictionaries representing the platform-specific posts.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def normalize_data(self, data):
        """
        Normalize platform-specific data to the common structure using the provided mapping.
        
        Args:
            data (list): List of dictionaries containing platform-specific post data.
        
        Returns:
            list: List of dictionaries with normalized post data.
        """
        normalized_data = []
        for post in data:
            normalized_post = {
                common_key: post.get(platform_key, "")  # Map platform-specific keys to common keys
                for common_key, platform_key in self.mapping.items()
            }
            normalized_data.append(normalized_post)
        return normalized_data

    def normalize(self):
        """
        Normalize the platform-specific data to the common structure.
        
        Returns:
            list: List of dictionaries with normalized post data.
        """
        # Load the raw data
        data = self.load_data()

        # Normalize the data using the mapping
        return self.normalize_data(data)