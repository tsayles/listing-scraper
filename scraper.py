import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from bs4 import BeautifulSoup

def get_links_from_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'path_to_credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1NdMsw3amImspKbzL25Ay6Xf1JWyPlL9PvMAh2u6eTfQ/edit?usp=sharing"
    ).sheet1
    headers = sheet.row_values(1)
    if 'Link' in headers:
        col_index = headers.index('Link') + 1
        links = sheet.col_values(col_index)[1:]
        return sheet, links
    else:
        raise ValueError('"Link" column not found in the sheet.')

def scrape_data(link):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get(link)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.quit()
    if "zillow.com" in link:
        # Update selectors based on Zillow's page structure
        status = soup.find('span', class_='Text-c11n-8-84-3__sc-aiai24-0 dpf__sc-1yftt2a-1 hrfydd ixkFNb').text
        asking = soup.find('span', class_='Text-c11n-8-84-3__sc-aiai24-0 dpf__sc-1me8eh6-0 OByUh fpfhCd').text
        sqft = soup.find('span', class_='Text-c11n-8-84-3__sc-aiai24-0 hrfydd').text
        address = soup.find('span', class_='Text-c11n-8-84-3__sc-aiai24-0 hrfydd').text
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
