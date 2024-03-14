from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time

def extract_data_from_page(soup, csv_writer):
    universities = soup.select('tbody tr')

    for university in universities:
        ranking_div = university.find('div', class_='ranking')
        world_rank = ranking_div.text.strip() if ranking_div else 'N/A'

        university_name = university.find('span', class_='univ-name').text.strip()

        region_img_style = university.find('div', class_='region-img')['style']
        country = region_img_style.split('/')[-1].replace('");', '').strip() if region_img_style else 'N/A'

        national_rank = university.find_all('td')[3].text.strip() if university.find_all('td') else 'N/A'
        total_score = university.find_all('td')[4].text.strip() if university.find_all('td') else 'N/A'

        csv_writer.writerow([world_rank, university_name, country, national_rank, total_score])

def scrape_all_pages(base_url, csv_filename):
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed and in your PATH

    # Open the CSV file for writing
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write the header row
        csv_writer.writerow(['World Rank', 'University Name', 'Country', 'National Rank', 'Total Score'])

        # Load the first page
        driver.get(base_url)
        time.sleep(2)  # Wait for dynamic content to load

        while True:
            # Get the page source after dynamic content loading
            page_source = driver.page_source

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract data from the page
            extract_data_from_page(soup, csv_writer)

            # Check if there is a "Next" button
            next_button = driver.find_element('css selector', 'li.ant-pagination-next')
            if 'ant-pagination-disabled' not in next_button.get_attribute('class'):
                # Click the "Next" button to load the next page
                next_button.click()
                time.sleep(2)  # Wait for dynamic content to load
            else:
                break

    # Close the Selenium WebDriver
    driver.quit()

base_url = "https://www.shanghairanking.com/rankings/arwu/2023"
csv_filename = "univ_rank.csv"
scrape_all_pages(base_url, csv_filename)
