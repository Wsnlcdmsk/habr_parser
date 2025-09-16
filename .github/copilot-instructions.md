# AI Coding Agent Instructions for `habr_parser`

## Overview
The `habr_parser` project is designed to scrape and process data from the Habr website. The codebase is structured to separate concerns across different modules, ensuring maintainability and scalability. The main components include:

- **Scraper**: Handles web scraping logic (`scraper.py`).
- **Processor**: Processes and transforms scraped data (`processor.py`).
- **Storage**: Manages data storage and retrieval (`storage.py`).
- **Utilities**: Contains helper functions (`utils.py`).
- **Configuration**: Centralized configuration settings (`config.py`).

## Key Developer Workflows

### Running the Project
To execute the main script:
```powershell
python habr_parser/main.py
```

### Installing Dependencies
Dependencies are listed in `requrements.txt`. Install them using:
```powershell
pip install -r requrements.txt
```

### Testing
Currently, no explicit test framework is set up. Add tests in a `tests/` directory and use `pytest` or another framework of your choice.

### Debugging
Use print statements or Python's built-in `pdb` module for debugging. For example, insert `import pdb; pdb.set_trace()` where needed.

## Project-Specific Conventions

- **Data Flow**: Scraped data flows from `scraper.py` to `processor.py` and is finally stored using `storage.py`.
- **Error Handling**: Ensure robust error handling, especially in `scraper.py`, to manage network issues or changes in the Habr website structure.
- **Logging**: Add logging for better traceability. Currently, no logging framework is integrated.

## Integration Points

- **External Dependencies**: The project relies on Python libraries specified in `requrements.txt`. Ensure these are up-to-date.
- **Cross-Component Communication**: Use function calls to pass data between modules. For example, `scraper.py` calls `processor.py` functions to process scraped data.

## Examples

### Scraper Pattern
The `scraper.py` file contains functions to fetch and parse HTML. Example:
```python
from bs4 import BeautifulSoup
import requests

def fetch_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')
```

### Processor Pattern
The `processor.py` file transforms raw data into structured formats. Example:
```python
def clean_data(raw_data):
    return raw_data.strip()
```

### Storage Pattern
The `storage.py` file saves data to disk or a database. Example:
```python
def save_to_file(data, filename):
    with open(filename, 'w') as f:
        f.write(data)
```

## Future Improvements
- Add automated tests.
- Integrate a logging framework.
- Enhance error handling in `scraper.py`.

---

Feel free to update this document as the project evolves.
