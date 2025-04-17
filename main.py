"""Extract and normalize posts from a <Platform> JSON file."""
import json
from post_normalizer import PostNormalizer

# Example usage
if __name__ == "__main__":
    # Path to the Telegram JSON file
    file_path = "./data/telegram.json"

    # Create an instance of PostNormalizer
    normalizer = PostNormalizer(file_path)

    # Normalize the data
    normalized_posts = normalizer.normalize()

    # Print the normalized data
    for post in normalized_posts:
        print(post)