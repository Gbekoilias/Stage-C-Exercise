
# URL of the webpage
url = "https://www.webometrics.info/en/Africa"

# Create CSV files to store the data for odd and even rows
csv_file_odd = open('webometric_data_odd.csv', 'w', newline='', encoding='utf-8')
csv_writer_odd = csv.writer(csv_file_odd)

csv_file_even = open('webometric_data_even.csv', 'w', newline='', encoding='utf-8')
csv_writer_even = csv.writer(csv_file_even)

# Write headers to the CSV files
csv_writer_odd.writerow(["Ranking", "World Rank", "University", "Det.", "Country", "Impact Rank", "Openness Rank", "Excellence Rank",
                        "World Ranking", "Continental Ranking", "Country Rank", "Impact", "Openness", "Excellence"])

csv_writer_even.writerow(["Ranking", "World Rank", "University", "Det.", "Country", "Impact Rank", "Openness Rank", "Excellence Rank",
                         "World Ranking", "Continental Ranking", "Country Rank", "Impact", "Openness", "Excellence"])

# Send a GET request to the webpage
response = requests.get(url)
response.encoding = response.apparent_encoding
soup = BeautifulSoup(response.text, 'html.parser')

# Find all table rows with the class "odd"
table_rows = soup.find_all('tr', class_=['odd', 'even'])

# Loop through each row in the table
for index, row in enumerate(table_rows, start=1):
    columns = row.find_all('td')
    ranking, world_rank, university, det, country, impact_rank, openness_rank, excellence_rank = [column.text.strip() for column in columns[:8]]

    # Check if 'det' is a button
    det_link = columns[3].find('a')
    if det_link:
        # If 'det' is a button, follow the link to the detail page
        detail_url = urljoin(url, det_link['href'])
        detail_response = requests.get(detail_url)
        detail_response.encoding = detail_response.apparent_encoding
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

        # Find the relevant details on the detail page
        detail_columns = detail_soup.find_all('td')
        
        # Check if there are enough columns to unpack the data
        if len(detail_columns) >= 6:
            world_ranking, continental_ranking, country_rank, impact, openness, excellence = [column.text.strip() for column in detail_columns[:6]]
        else:
            # If there are not enough columns, fill in empty values for detail information
            world_ranking, continental_ranking, country_rank, impact, openness, excellence = ["", "", "", "", "", ""]
    else:
        # If 'det' is not a button, fill in empty values for detail information
        world_ranking, continental_ranking, country_rank, impact, openness, excellence = ["", "", "", "", "", ""]

    # Determine if the row is odd or even based on the index
    if index % 2 == 1:
        # Odd row
        csv_writer_odd.writerow([ranking, world_rank, university, det, country, impact_rank, openness_rank, excellence,
                                world_ranking, continental_ranking, country_rank, impact, openness, excellence])
    else:
        # Even row
        csv_writer_even.writerow([ranking, world_rank, university, det, country, impact_rank, openness_rank, excellence,
                                 world_ranking, continental_ranking, country_rank, impact, openness, excellence])

# Close the CSV files
csv_file_odd.close()
csv_file_even.close()
