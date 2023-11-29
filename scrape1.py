#import relevant libraries
import requests
from  bs4 import BeautifulSoup as bs
import json
import pandas as pd
import csv
import re
import random
url = 'https://www.webometrics.info/en/Africa'
# Create a CSV file to store the data
csv_file = open('webometric_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

# Write headers to the CSV file
csv_writer.writerow(["Ranking", "World Rank", "University", "Det.", "Country", "Impact Rank", "Openness Rank", "Excellence Rank",
                    "World Ranking", "Continental Ranking", "Country Rank", "Impact", "Openness", "Excellence"])

# Loop through 20 pages
for page_num in range(1, 21):
    page_url = f"https://www.webometrics.info/en/Africa?page={page_num}"

    # Send a GET request to the page
    response = requests.get(page_url)
    soup = bs(response.text, 'html.parser')

    # Find the table containing the data
    table = soup.find('table', {'class': 'table'})
    rows = table.find_all('tr')

    # Loop through each row in the table
    for row in rows[1:]:  # Skip the header row
        columns = row.find_all('td')
        ranking, world_rank, university, det, country, impact_rank, openness_rank, excellence_rank = [column.text.strip() for column in columns[:8]]

        # Check if 'det' is a button
        det_link = columns[3].find('a')
        if det_link:
            # If 'det' is a button, follow the link to the detail page
            detail_url = det_link['href']
            detail_response = requests.get(detail_url)
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

            # Find the relevant details on the detail page
            detail_columns = detail_soup.find_all('td')
            world_ranking, continental_ranking, country_rank, impact, openness, excellence = [column.text.strip() for column in detail_columns[:6]]
        else:
            # If 'det' is not a button, fill in empty values for detail information
            world_ranking, continental_ranking, country_rank, impact, openness, excellence = ["", "", "", "", "", ""]

        # Write the data to the CSV file
        csv_writer.writerow([ranking, world_rank, university, det, country, impact_rank, openness_rank, excellence,
                            world_ranking, continental_ranking, country_rank, impact, openness, excellence])

# Close the CSV file
csv_file.close()
