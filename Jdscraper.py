import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# URL and headers
url = "https://www.justdial.com/Mumbai/Dentists/nct-10156331"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.google.com'
}
# Send request and parse HTML
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

# Extract data
search_query = soup.select("h1.jsx-7cc2aa6b721daec4.font22.fw500.color111.line_clamp_1")
location = soup.select_one("input.input_location.font14.fw400.color111")
data_collection = soup.select("div.jsx-98ac5e1b53154d9c.resultbox_info")
location_value = location.get('value') if location else 'NIL'
# Process search query
if search_query:
    search_query_text = search_query[0].text.strip()
    match = re.search(r'Best (.*?) in', search_query_text) or re.search(r'Popular (.*?) in', search_query_text)
    extracted_text = match.group(1) if match else 'NIL'
else:
    extracted_text = 'NIL'

# Initialize lists
names = []
phone_numbers = []
my_address = []
amenities = []
people_enquiry=[]
ratings_got=[]

# Extract names, phone numbers, addresses, and amenities
for data in data_collection [:10]:
    # Extract name
    name_tag = data.select_one("div.jsx-98ac5e1b53154d9c.resultbox_title_anchor.line_clamp_1")
    name = name_tag.text.strip() if name_tag else 'NIL'
    names.append(name)

    # Extract phone number
    phone_tag = data.select_one("span.jsx-98ac5e1b53154d9c.callcontent.callNowAnchor")
    contact = phone_tag.text.strip() if phone_tag else 'NIL'
    phone_numbers.append(contact)
    # Extract address
    address_tag = data.select_one("div.jsx-98ac5e1b53154d9c.font15.fw400.color111")
    addr = address_tag.text.strip() if address_tag else 'NIL'
    my_address.append(addr)

    # Extract amenities
    amenities_tags = data.select("div.jsx-98ac5e1b53154d9c.amenities_tabs.font12.fw500.color777")
    amenities_texts = [tag.text.strip() for tag in amenities_tags]
    amenities.append(", ".join(amenities_texts) if amenities_texts else 'NIL')

    #People Enquired
    people_enquired=data.select("div.jsx-98ac5e1b53154d9c.font12.fw500.color111")
    for peoples in people_enquired:
        peoples_enquiry=peoples.text.strip() if peoples else 'NIL'
    people_enquiry.append(peoples_enquiry)

    # Ratings
    ratings=data.select("div.jsx-98ac5e1b53154d9c.resultbox_totalrate.mr-6.font14.fw700.colorFFF")
    for rate in ratings:
        raters=rate.string
        ratings_got.append(raters)

max_length = max(len(names), len(phone_numbers), len(my_address), len(amenities),len(people_enquiry),len(ratings_got))
names.extend(['NIL'] * (max_length - len(names)))
phone_numbers.extend(['NIL'] * (max_length - len(phone_numbers)))
my_address.extend(['NIL'] * (max_length - len(my_address)))
amenities.extend(['NIL'] * (max_length - len(amenities)))
people_enquiry.extend(['NIL'] * (max_length - len(people_enquiry)))
ratings_got.extend(['NIL'] * (max_length - len(ratings_got)))

# Create DataFrame
data = {
    'Search Query': [extracted_text] * max_length,
    'Names': names,
    'Phone Number': phone_numbers,
    'Address': my_address,
    'Services': amenities,
    'People Enquired': people_enquiry,
    'Ratings': ratings_got,
    'Location': [location_value] * max_length
}
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('justdial_scrapped.csv', index=False)

print("DataFrame saved to CSV successfully.")