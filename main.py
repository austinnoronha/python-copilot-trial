"""Extract and normalize posts from a <Platform> JSON file."""
import json
from post_normalizer import PostNormalizer

def load_print_data(file_path, mapping):
    """Load and print normalized data from a JSON file."""
    
    print(f"Loading data from {file_path}...")
    
    # Create an instance of PostNormalizer with the mapping
    normalizer = PostNormalizer(file_path, mapping)

    # Normalize the data
    normalized_posts = normalizer.normalize()

    # Print the normalized data
    for post in normalized_posts:
        print(post)

def main():
    """Main function to process and normalize data for multiple platforms."""
    
    # Load platform mappings from the JSON configuration file
    with open('./data/platform_mappings.json', 'r', encoding='utf-8') as config_file:
        platform_configs = json.load(config_file)

    # Iterate over each platform configuration and process the data
    for platform, config in platform_configs.items():
        print(f"\nProcessing data for {platform}...\n")
        load_print_data(config["file_path"], config["mapping"])
        print("\n" + "=" * 40 + "\n")
        
        
    # Example usage for a specific platform (e.g., Telegram)
    print("\nProcessing data for Telegram only...\n")
    load_print_data(file_path=platform_configs['Telegram']["file_path"],
                    mapping=platform_configs['Telegram']["mapping"])
    print("\n" + "=" * 40 + "\n")
        

if __name__ == "__main__":
    main()

