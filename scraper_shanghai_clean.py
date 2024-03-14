import pandas as pd
import re

def clean_university_name(name):
    # Clean non-alphabet characters
    return re.sub(r'[^a-zA-Z\s]', '', name)

def clean_country(country):
    # Extract country code from the provided format (e.g., 'us.png')
    country_code = re.search(r'([a-zA-Z]+)\.png', country)
    if country_code:
        return country_code.group(1).upper()
    else:
        return country

# Read the original CSV file
input_file = 'univ_rank.csv'
df = pd.read_csv(input_file)

# Apply cleaning functions to relevant columns
df['University Name'] = df['University Name'].apply(clean_university_name)
df['Country'] = df['Country'].apply(clean_country)

# Add a new column for incremented World Rank
df['World Rank'] = range(1, len(df) + 1)

# Save the cleaned data to a new CSV file
output_file = 'univ_rank_clean.csv'
df.to_csv(output_file, index=False)

print(f"Cleaning completed. Cleaned data saved to {output_file}")
