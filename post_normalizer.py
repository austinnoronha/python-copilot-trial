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

import json

class PostNormalizer:
    """A class to normalize post data from different platforms into a common structure."""

    def __init__(self, file_path):
        """
        Initialize the PostNormalizer with the path to the platform's JSON file.
        
        Args:
            file_path (str): Path to the JSON file containing platform-specific data.
        """
        self.file_path = file_path

    def load_data(self):
        """
        Load JSON data from the specified file path.
        
        Returns:
            list: A list of dictionaries representing the platform-specific posts.
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def normalize_telegram_data(self, data):
        """
        Normalize Telegram-specific data to the common structure.
        
        Args:
            data (list): List of dictionaries containing Telegram-specific post data.
        
        Returns:
            list: List of dictionaries with normalized post data.
        """
        normalized_data = []
        for post in data:
            normalized_post = {
                "text": post.get("tel_text", ""),  # Original text
                "summary": post.get("tel_text_summary", ""),  # Summary of the text
                "translated_text": post.get("tel_text_translation", ""),  # Translated text
                "media_url": post.get("media_url", "")  # Media URL
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

        # Check the file name to determine the platform and normalize accordingly
        if "telegram" in self.file_path.lower():
            return self.normalize_telegram_data(data)
        else:
            raise NotImplementedError("Normalization for this platform is not implemented yet.")