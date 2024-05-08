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

    while True:
        response = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr', {'role': 'row'})[1:]  # Skip header row

        for row in rows:
            columns = row.find_all('td')
            if columns:
                bid_number_link = columns[0].find('a', href=True)['href']
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

                bid_page_url = "https://nevadaepro.com" + bid_number_link
                bid_response = requests.get(bid_page_url, headers=headers)
                bid_soup = BeautifulSoup(bid_response.text, 'html.parser')

                files = bid_soup.find_all('a', text='Download')
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

        next_button = soup.find('a', text='Next')
        if next_button and 'disabled' not in next_button.parent.get('class', []):
            base_url = "https://nevadaepro.com" + next_button['href']
        else:
            break

    with open('nevada_epro_bids.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)

if __name__ == '__main__':
    scrape_nevada_epro()
