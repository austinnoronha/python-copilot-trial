# Python Post Normalizer (Sample)

## Overview
The **Platform Post Normalizer** is a Python application designed to process and normalize post data from various social media platforms. Each platform has its own JSON data structure, and this application maps those structures to a common format (`text`, `summary`, `translated_text`, `media_url`) for easier processing and analysis.

## Features
- **Platform-Agnostic Normalization**: Supports multiple platforms with different JSON structures.
- **Configurable Mappings**: Platform-specific mappings are stored in a separate JSON configuration file, making the application extensible and easy to maintain.
- **Scalable Design**: Adding support for new platforms requires only updating the configuration file without modifying the core logic.

---

## Install
```bash
cd __git_folder_path/

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Project Structure
```
├── main.py                     # Main script to process and normalize data
├── post_normalizer.py          # Class to handle normalization logic
├── config
│   └── platform_mappings.json  # Configuration file for platform-specific mappings
├── data
│   ├── telegram.json           # Example data file for Telegram
│   └── twitter.json            # Example data file for Twitter
└── README.md                   # Project documentation
```

---

## Usage
1. Add your platform-specific JSON files to the `data` folder.
2. Update the `config/platform_mappings.json` file with the file paths and mappings for each platform.
3. Run the `main.py` script:
   ```bash
   python main.py
   ```

---

## Example Output
For the `Telegram` platform, the normalized output might look like this:
```
Processing data for Telegram...

{'text': 'Join our channel for daily crypto updates 🚀', 'summary': 'Daily updates on cryptocurrency trends and prices.', 'translated_text': '', 'media_url': 'https://pbs.twimg.com/media/Fv8e0mWakAYPfd1.jpg'}
{'text': 'Of the 33,000-plus donors on @ossoff\'s disclosure', 'summary': 'Disclosure about a large group of donors.', 'translated_text': '', 'media_url': 'https://pbs.twimg.com/media/Fp4x7hBXsAMsOa5.jpg'}
...

========================================
```

---

## Adding a New Platform
1. Add the platform's JSON file to the `data` folder.
2. Update the `config/platform_mappings.json` file with the new platform's file path and key mappings.
3. Run the `main.py` script to process the new platform.

---

## Extensibility
- **New Platforms**: Add new platforms by updating the `platform_mappings.json` file.
- **Custom Logic**: Extend the `PostNormalizer` class if platform-specific custom logic is required.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author
Developed by Austin.