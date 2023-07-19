import requests, json
from bs4 import BeautifulSoup

def process_result(listing):
  return {
    # "id": listing['id'],
    # "date": listing['date'],
    # "modified": listing['modified'],
    # "slug": listing['slug'],
    'link': listing['link'],
    # "status": listing['status'],
    "title": BeautifulSoup(listing['title']['rendered'], features="html.parser").get_text(),
    # "content": BeautifulSoup(listing['content']['rendered'], features="html.parser").get_text(),
    "price": listing['listivo_130'],
    # "lot-size": listing['listivo_9694'],
    "area": listing['listivo_9508'][0] if listing['listivo_9508'] else "unspecified",
    # "land-size": listing['listivo_5991'][0] if listing['listivo_5991'] else "unspecified",
    "bathrooms": listing['listivo_5463'][0] if listing['listivo_5463'] else "unspecified",
    "bedrooms": listing['listivo_5462'][0] if listing['listivo_5462'] else "unspecified",
    # "property-features": listing['listivo_4661'],
    # "property-size": listing['listivo_340'][0] if listing['listivo_340'] else "unspecified",
    "location": listing['listivo_153'],
    # "property-type": listing['listivo_14']
  }


def get_listings(params):
  url = 'https://gojo.rent/wp-json/wp/v2/listings/'
  response = requests.get(url, params=params)
  if response.status_code == 200:
      data = response.json()
      return json.dumps(list(map(process_result, data))[:5])
  else:
      print('Error: Failed to retrieve data')
      return []
