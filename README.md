# Gazette Notice Scraper

## Overview
This Python script is designed to automatically crawl and extract data from notice pages on The Gazette's website. It navigates through pages 1 to 15, accessing individual notices to gather detailed information such as notice details, deceased details, last address of the deceased, and executor/administrator details. The extracted data is then organized and saved into a CSV file for easy access and analysis.

## Features
- Crawls through specified pages of The Gazette's notice section.
- Extracts detailed information from each notice:
  - Notice Details (Type, Notice Type, Publish Date, etc.)
  - Deceased Details (Name, Date of Death, etc.)
  - Last Address of the Deceased
  - Executor/Administrator Details
- Handles web requests responsibly with appropriate delays.
- Saves the extracted data into a CSV file.

## Requirements
- Python 3.6+
- BeautifulSoup4: For parsing HTML and extracting the required information.
- Requests: For making HTTP requests to The Gazette's website.
- Pandas: For organizing the extracted data and saving it into a CSV file.

To install the necessary libraries, run:
```bash
pip install beautifulsoup4 requests pandas
```

## Usage
1. Ensure you have Python 3.6+ installed on your system.
2. Install the required Python libraries mentioned above.
3. Save the script to a local file, for example, `gazette_scraper.py`.
4. Open a terminal or command prompt.
5. Navigate to the directory where the script is saved.
6. Run the script using Python:

   ```bash
   python gazette_scraper.py
   ```
8. Once the script completes its execution, you will find a CSV file named `extracted_notices.csv` in the same directory, containing all the extracted data.

## Configuration
The script is configured to scrape the first 15 pages of The Gazette's notice section by default. You can modify the `PARAMS` dictionary within the script to change the search criteria, such as categories, notice types, location details, and date ranges.

## Disclaimer
This script is provided for educational purposes only. Always respect The Gazette's `robots.txt` file and terms of service when scraping their website. Ensure that your use of this script complies with their policies and legal requirements.

## Support
For questions or issues regarding the script, please open an issue on the GitHub repository where this script is hosted.
