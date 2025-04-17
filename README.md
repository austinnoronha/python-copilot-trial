# Python Post Normalizer (Sample)

## Overview
The **Platform Post Normalizer** is a Python Flask application designed to process and normalize post data from various social media platforms. Each platform has its own JSON data structure, and this application maps those structures to a common format (`text`, `summary`, `translated_text`, `media_url`) for easier processing and analysis.

## Features
- **Platform-Agnostic Normalization**: Supports multiple platforms with different JSON structures.
- **Configurable Mappings**: Platform-specific mappings are stored in a separate JSON configuration file, making the application extensible and easy to maintain.
- **Scalable Design**: Adding support for new platforms requires only updating the configuration file without modifying the core logic.
- **XSS Prevention**: Input sanitization and validation to prevent XSS attacks.
- **Custom Error Handling**: Handles `404` and `500` errors gracefully with meaningful error messages.

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
├── app.py                      # Flask application with API endpoints
├── post_normalizer.py          # Class to handle normalization logic
├── config
│   └── platform_mappings.json  # Configuration file for platform-specific mappings
├── data
│   ├── telegram.json           # Example data file for Telegram
│   └── twitter.json            # Example data file for Twitter
├── tests
│   └── test_app.py             # Unit tests for the Flask application
└── README.md                   # Project documentation
```

---

## Usage
1. Add your platform-specific JSON files to the `data` folder.
2. Update the `config/platform_mappings.json` file with the file paths and mappings for each platform.
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Access the API endpoints:
   - `GET /`: Returns normalized posts for all platforms.
   - `GET /<platform>`: Returns normalized posts for a specific platform (e.g., `/Telegram`).

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

## API Endpoints
### 1. `GET /`
- **Description**: Returns normalized posts for all platforms.
- **Response**:
  - `200 OK`: List of normalized posts.
  - `500 Internal Server Error`: If the configuration file is missing or invalid.

### 2. `GET /<platform>`
- **Description**: Returns normalized posts for a specific platform.
- **Parameters**:
  - `<platform>`: The name of the platform (e.g., `Telegram`, `Twitter`).
- **Response**:
  - `200 OK`: List of normalized posts for the specified platform.
  - `400 Bad Request`: If the platform name is invalid or unsupported.
  - `500 Internal Server Error`: If the configuration file is missing or invalid.

### 3. Error Handling
- **404 Not Found**: Returned when an invalid route is accessed.
  ```json
  {
      "error": "The requested resource was not found"
  }
  ```

---

## Adding a New Platform
1. Add the platform's JSON file to the `data` folder.
2. Update the `config/platform_mappings.json` file with the new platform's file path and key mappings.
3. Restart the Flask application to process the new platform.

---

## Extensibility
- **New Platforms**: Add new platforms by updating the `platform_mappings.json` file.
- **Custom Logic**: Extend the `PostNormalizer` class if platform-specific custom logic is required.

---

## Testing
Unit tests are provided to ensure the application works as expected. The tests cover:
- Functional test cases for successful responses.
- Negative test cases for invalid input or missing files.
- Security test cases for XSS prevention.

### Run Tests
1. Install `pytest`:
   ```bash
   pip install pytest
   ```
2. Run the tests:
   ```bash
   pytest tests/test_app.py
   ```

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author
Developed by Austin.