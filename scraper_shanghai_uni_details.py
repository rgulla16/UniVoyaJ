import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_univ_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        details_container = soup.select_one('.contact-msg')
        intro_container = soup.select_one('.school-introduction p')
        if details_container and intro_container:
            details = {
                'University Name': get_detail(soup, '.name-en'),
                'Region': get_detail(details_container, '.contact-item span', index=1),
                'Country': get_detail(details_container, '.contact-item span', index=3),
                'Found Year': get_detail(details_container, '.contact-item span', index=5),
                'Address': get_detail(details_container, '.contact-item span', index=7),
                'Website': get_detail(details_container, '.contact-item a', index=0),
                'Introduction': intro_container.text.strip()
            }
            return details
        else:
            print(f"Details or Introduction container not found for {url}")
            return None
    else:
        print(f"Failed to fetch details for {url}")
        return None

def get_detail(soup, selector, index=0):
    elements = soup.select(selector)
    if elements and index < len(elements):
        return elements[index].text.strip()
    else:
        return None

# Read the cleaned university data
input_file = 'univ_rank_clean.csv'
df = pd.read_csv(input_file)

# Initialize an empty list to store details
details_list = []

# Loop through each row in the dataframe
for index, row in df.iterrows():
    university_name = row['University Name']
    # Generate the URL
    url = f'https://www.shanghairanking.com/institution/{university_name.lower().replace(" ", "-")}'
    univ_details = get_univ_details(url)

    # Append details to the list
    if univ_details:
        details_list.append(univ_details)

# Create a new DataFrame from the list
details_df = pd.DataFrame(details_list)

# Save the details DataFrame to a new CSV file
details_df.to_csv('univ_details.csv', index=False)

print("University details extraction completed. Details saved to univ_details.csv")
