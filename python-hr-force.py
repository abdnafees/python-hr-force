import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from time import sleep

# Base URL setup
BASE_URL = "https://www.thegazette.co.uk/all-notices/notice"
PARAMS = {
    "text": "",
    "categorycode-all": "all",
    "noticetypes": "",
    "location-postcode-1": "",
    "location-distance-1": "1",
    "location-local-authority-1": "",
    "numberOfLocationSearches": "1",
    "start-publish-date": "",
    "end-publish-date": "",
    "edition": "",
    "london-issue": "",
    "edinburgh-issue": "",
    "belfast-issue": "",
    "sort-by": "",
    "results-page-size": "10",
    "page": 0
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Placeholder for the extracted data
extracted_data = []

# Crawl pages from 1 to 15
for page in range(1, 16):
    print(f"Crawling page {page}...")
    PARAMS["page"] = page  # Update page parameter for pagination
    response = requests.get(BASE_URL, headers=headers, params=PARAMS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        notices = soup.find_all("a", class_="btn btn-full-notice", href=True)  # Assuming notices are links; adjust selector as needed
        for notice in notices:
            notice_url = urljoin(BASE_URL, notice['href'])
            notice_response = requests.get(notice_url, headers=headers)
            if notice_response.status_code == 200:
                notice_soup = BeautifulSoup(notice_response.text, 'html.parser')
                notice_data = {
                    "notice_details": {},
                    "deceased_details": {},
                    "last_address_of_deceased": {},
                    "executor_administrator_details": {},
                }
                # Notice Details Extraction
                notice_summary = notice_soup.find("div", class_="notice-summary")
                if notice_summary:
                    dl_items = notice_summary.find_all("dl")
                    for dl in dl_items:
                        dts = dl.find_all("dt")
                        dds = dl.find_all("dd")
                        for dt, dd in zip(dts, dds):
                            key = dt.text.strip(':')
                            value = dd.text.strip()
                            notice_data["notice_details"][key] = value

                # Full Notice Details Extraction (with defensive checks)
                sections = notice_soup.find_all("section")
                for section in sections:
                    header = section.find("header")
                    if header:  # Check if header is found
                        header_text = header.text.lower()  # Safe to access .text
                        # Identifying the section based on header text
                        target_dict = None
                        if 'deceased' in header_text:
                            target_dict = "deceased_details"
                        elif 'last address' in header_text:
                            target_dict = "last_address_of_deceased"
                        elif 'executor' in header_text or 'administrator' in header_text:
                            target_dict = "executor_administrator_details"

                        if target_dict:  # Proceed only if a target section is identified
                            dls = section.find_all("dl")
                            for dl in dls:
                                dts = dl.find_all("dt")
                                dds = dl.find_all("dd")
                                for dt, dd in zip(dts, dds):
                                    key = dt.text.strip(':').strip()
                                    value = dd.text.strip()
                                    notice_data[target_dict][key] = value
                                    extracted_data.append(notice_data)

            sleep(10)  # Respectful crawling by sleeping between requests
    else:
        print(f"Failed to fetch page {page}. Status code: {response.status_code}")

# Convert extracted data to a DataFrame
df = pd.DataFrame(extracted_data)

# Save data to CSV
csv_file_path = "extracted_notices.csv"
df.to_csv(csv_file_path, index=False)
print(f"Data extraction completed. Saved to {csv_file_path}.")
