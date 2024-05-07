import os
import json
import requests
from bs4 import BeautifulSoup


def scrape_nevada_epro():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    base_url = "https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true"
    result = []
    while True:import os
import json
import requests
from bs4 import BeautifulSoup


def scrape_nevada_epro():
    """
    Scrapes bid information and downloads attachments from the Nevada EPro website.
    
    :return: None
    """
    # Set user-agent to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    # Base URL for scraping
    base_url = "https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true"
    
    # List to store scraped data
    result = []
    
    # Loop through all pages
    while True:
        # Get HTML response
        response = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract data from the first page
        rows = soup.find_all('tr', {'role': 'row'})[1:]  # skip header row
        for row in rows:
            columns = row.find_all('td')
            if columns:
                # Extract bid information
                bid_number_link = columns[0].find('a')['href']
                bid_number = columns[0].get_text(strip=True)
                buyer = columns[1].get_text(strip=True)
                description = columns[2].get_text(strip=True)
                bid_open_date = columns[3].get_text(strip=True)
                
                # Create dictionary to store bid details
                bid_details = {
                    'Bid Number': bid_number,
                    'Buyer': buyer,
                    'Description': description,
                    'Bid Opening Date': bid_open_date,
                    'Attachments': []
                }
                
                # Navigate to individual bid page
                bid_page_url = "https://nevadaepro.com" + bid_number_link
                bid_response = requests.get(bid_page_url, headers=headers)
                bid_soup = BeautifulSoup(bid_response.text, 'html.parser')
                headers = bid_soup.find_all('h3')  # Assuming headers are h3, modify if necessary

                for header in headers:
                    # Extract header details till "Bill-to Address"
                    if header.text.strip() == "Bill-to Address":
                        break
                    next_sib = header.find_next_sibling()
                    if next_sib and next_sib.name in ['p', 'div']:
                        bid_details[header.text.strip()] = next_sib.get_text(strip=True)
                
                # Download attachments
                files = bid_soup.find_all('a', string='Download')
                for file in files:
                    file_url = "https://nevadaepro.com" + file['href']
                    file_response = requests.get(file_url, headers=headers)
                    file_name = file['href'].split('/')[-1]
                    folder_path = os.path.join('downloads', bid_number)
                    os.makedirs(folder_path, exist_ok=True)
                    file_path = os.path.join(folder_path, file_name)
                    
                    with open(file_path, 'wb') as f:
                        f.write(file_response.content)
                    bid_details['Attachments'].append(file_path)

                result.append(bid_details)

        # Pagination handling
        next_button = soup.find('a', string='Next')
        if next_button and 'disabled' not in next_button.parent.get('class', []):
            base_url = "https://nevadaepro.com" + next_button['href']
        else:
            break

    # Save results to JSON
    with open('nevada_epro_bids.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)

if __name__ == '__main__':
    scrape_nevada_epro()

        response = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract data from the first page
        rows = soup.find_all('tr', {'role': 'row'})[1:]  # skip header row
        for row in rows:
            columns = row.find_all('td')
            if columns:
                bid_number_link = columns[0].find('a')['href']
                bid_number = columns[0].get_text(strip=True)
                buyer = columns[1].get_text(strip=True)
                description = columns[2].get_text(strip=True)
                bid_open_date = columns[3].get_text(strip=True)
                
                bid_details = {
                    'Bid Number': bid_number,
                    'Buyer': buyer,
                    'Description': description,
                    'Bid Opening Date': bid_open_date,
                    'Attachments': []
                }
                
                # Navigate to individual bid page
                bid_page_url = "https://nevadaepro.com" + bid_number_link
                bid_response = requests.get(bid_page_url, headers=headers)
                bid_soup = BeautifulSoup(bid_response.text, 'html.parser')
                headers = bid_soup.find_all('h3')  # Assuming headers are h3, modify if necessary

                for header in headers:
                    if header.text.strip() == "Bill-to Address":
                        break
                    next_sib = header.find_next_sibling()
                    if next_sib and next_sib.name in ['p', 'div']:
                        bid_details[header.text.strip()] = next_sib.get_text(strip=True)
                
                # Download attachments
                files = bid_soup.find_all('a', string='Download')
                for file in files:
                    file_url = "https://nevadaepro.com" + file['href']
                    file_response = requests.get(file_url, headers=headers)
                    file_name = file['href'].split('/')[-1]
                    folder_path = os.path.join('downloads', bid_number)
                    os.makedirs(folder_path, exist_ok=True)
                    file_path = os.path.join(folder_path, file_name)
                    
                    with open(file_path, 'wb') as f:
                        f.write(file_response.content)
                    bid_details['Attachments'].append(file_path)

                result.append(bid_details)

        # Pagination handling
        next_button = soup.find('a', string='Next')
        if next_button and 'disabled' not in next_button.parent.get('class', []):
            base_url = "https://nevadaepro.com" + next_button['href']
        else:
            break

    # Save results to JSON
    with open('nevada_epro_bids.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)

if __name__ == '__main__':
    scrape_nevada_epro()
