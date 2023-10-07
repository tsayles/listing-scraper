import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup

def get_links_from_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1NdMsw3amImspKbzL25Ay6Xf1JWyPlL9PvMAh2u6eTfQ/edit?usp=sharing").sheet1
    headers = sheet.row_values(1)
    if 'Link' in headers:
        col_index = headers.index('Link') + 1
        links = sheet.col_values(col_index)[1:]
        return sheet, links
    else:
        raise ValueError('"Links" column not found in the sheet.')

def scrape_data(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    if "zillow.com" in link:
        status = soup.find('span', class_='status').text
        asking = soup.find('span', class_='price').text
        sqft = soup.find('span', class_='sqft').text
        address = soup.find('span', class_='address').text
    elif "redfin.com" in link:
        status = soup.find('span', class_='status').text
        asking = soup.find('span', class_='price').text
        sqft = soup.find('span', class_='sqft').text
        address = soup.find('span', class_='address').text
    elif "onehome.com" in link:
        status = soup.find('span', class_='status').text
        asking = soup.find('span', class_='price').text
        sqft = soup.find('span', class_='sqft').text
        address = soup.find('span', class_='address').text
    else:
        return None
    return status, asking, sqft, address

def update_sheet(sheet, row, data):
    for i, value in enumerate(data, start=2):
        sheet.update_cell(row, i, value)

def main():
    sheet, links = get_links_from_sheet()
    for idx, link in enumerate(links, start=2):
        data = scrape_data(link)
        if data:
            update_sheet(sheet, idx, data)

if __name__ == "__main__":
    main()
