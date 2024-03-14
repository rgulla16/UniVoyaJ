import requests
from bs4 import BeautifulSoup

url = "https://www.shanghairanking.com/rankings/arwu/2023"

# Send a GET request to the URL
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using 'html.parser'
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the relevant elements containing the data
    universities = soup.select('tbody tr')  # Use 'tbody tr' to select table rows directly

    # Loop through the universities and extract the required information
    for university in universities:
        world_rank = university.find('div', class_='ranking').text.strip()
        university_name = university.find('span', class_='univ-name').text.strip()
        country = university.find('div', class_='region-img')['style'].split('/')[-1].replace('");', '').strip()
        national_rank = university.find_all('td')[3].text.strip()
        total_score = university.find_all('td')[4].text.strip()

        # Print or process the extracted information as needed
        print(f"World Rank: {world_rank}")
        print(f"University Name: {university_name}")
        print(f"Country: {country}")
        print(f"National Rank: {national_rank}")
        print(f"Total Score: {total_score}")
        print("-" * 30)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
