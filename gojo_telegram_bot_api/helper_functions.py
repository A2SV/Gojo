# Helper functions for preparing search parameters to listivo API
from rapidfuzz import fuzz
# Making API calls to the listivo api (this will be called using parameters from the chat app)
import requests, json
# Function to process the html results from the listivo API call into a desired format
from bs4 import BeautifulSoup
# Import function definitions
from function_definitions import function_definitions

import pygsheets
functions = function_definitions
# Function to save a listing on the Gojo Temporary Storage google sheet for review.
# the file gojo-service-account.json should exist in the same folder for authentication. (this is generated from google cloud as a key for a service account)

gc = pygsheets.authorize(service_file='gojo-service-account.json')
document = gc.open_by_key('1hwTUgyyRxKNsnoxQXbQZr2KcaYSWI5fVYxiModOnvvM')
worksheet = document[0]
columns = ["landlord-name", "landlord-contact", "telegram-id", "property-type", "title", "description", "price", "location", "bathrooms", "bedrooms", "property-features", "keywords"]
# worksheet.insert_rows(0, values=columns)

def add_listing_to_sheet(listing):
  print("adding called")
  try:
    ordered_listing = [listing.get(key) for key in columns]
    worksheet.insert_rows(worksheet.rows, values=ordered_listing, inherit=True)
  except:
    return "Error adding listing. Please try again"
  return "Successfully added to drafts. It will be put on the Gojo platform when approved."

property_type_map = {
  "apartment": 425,
  "office": 428,
  "house": 424,
  "service house": 426,
  "condominium": 431,
}

property_feature_map = {
  "administrative support": 263,
  "allows stove and oven": 267,
  "broadband internet": 268,
  "security system": 285,
  "balcony": 266,
  "ceiling fan": 269,
  "edir": 264,
  "garden": 277,
  "high ceilings": 278,
  "lift": 282,
  "furnished": 276,
  "wifi": 287,
}

def find_property_type(type_string):
  for type_name, type_id in property_type_map.items():
    if fuzz.ratio(type_name.lower(), type_string.lower()) >= 90:
      return type_id
  return None

def find_property_features(feature_strings):
  results = []
  for feature_string in feature_strings:
    for feature_name, feature_id in property_feature_map.items():
      if fuzz.ratio(feature_name.lower(), feature_string.lower()) >= 90:
        return results.append(feature_id)
  return results

def flatten_dict(data, parent_key=''):
    items = []
    if type(data) is list:
      for index, value in enumerate(data):
        new_key = f"{parent_key}[{index}]"
        items.extend(flatten_dict(value, new_key))
    elif type(data) is dict:
      for key, value in data.items():
        new_key = f"{parent_key}[{key}]" if parent_key else key
        items.extend(flatten_dict(value, new_key))
    else:
      items.append((parent_key, data))
    return items

# Preparing simple search parameters for sending to Listvo API

def format_params(simple_params):
  # shape of simple filters
  # { # location filters may need figuring out
  #   'location-place-id': 'GhIJE-EVd3IMIkARe1aI_VRiQ0A',
  #   'location-sw-lat': 8.753463145705288,
  #   'location-sw-lng': 38.49396144583313,
  #   'location-ne-lat': 9.295161854294712,
  #   'location-ne-lng': 39.042415594895786,
  #   'location-radius': 30000,

  #   'price-from': 5000,
  #   'price-to': 5500,
  #   'property-type': 'apartments',
  #   'property-features': ['Oven', 'Lift'],
  #   'bedrooms-from': 2,
  #   'bathrooms-from': 2
  #   }


  filters = []
  if 'price-from' in simple_params:
    filters.append(
        {
          "key": "listivo_130_from",
          "values": [simple_params["price-from"]],
          "compareType": "greater"
        },
        )
  if 'price-to' in simple_params:
    filters.append(
        {
          "key": "listivo_130_to",
          "values": [simple_params["price-to"]],
          "compareType": "less"
        },
        )
  if 'bedrooms-from' in simple_params:
    filters.append(
        {
        "key": "listivo_5462_from",
        "values": [simple_params['bedrooms-from']],
        },
        )
  if 'bathrooms-from' in simple_params:
    filters.append(
      {
        "key": "listivo_5463_from",
        "values": [simple_params['bathrooms-from']],
      },
      )

  if 'property-type' in simple_params:
    type_id = find_property_type(simple_params['property-type'])
    if type_id is not None:
      filters.append(
          {
            "key": "listivo_14",
            "values": [type_id],
          }
        )

  if 'property-features' in simple_params:
    feature_ids = find_property_features(simple_params['property-features'])
    if feature_ids:
      filters.append(
          {
            "key": "listivo_4661",
            "values": feature_ids,
          }
        )

  return flatten_dict({
      "template": "templates/partials/search_results_row_regular_v2",
      "cardType": "card_regular",
      "rowType": "row_regular_v2",
      "params": {
          "page": int(simple_params['page']) if 'page' in simple_params else 1,
          "limit": 5,
          "sortBy": "most-relevant"
          },
      "map": 0,
      "locationFieldId": 0,

      "filters": filters
  })


# Function to process the html results from the listivo API call into a desired format

def process_results(api_result):
  def process_one_result(listing_card):
    image_divs = listing_card.find_all('div', class_="listivo-swiper-slide")
    def parse_image_link(img_div):
      img = img_div.find("img")
      if img.has_attr("data-src"):
        return img["data-src"]
      elif img.has_attr("data-srcset"):
        return img["data-srcset"].split(",")[0].split(" ")[0]
      return None

    properties = dict(map(lambda x: x.get_text().strip().split(": "),
                          listing_card.find_all('div', class_="listivo-listing-card-row-v2__category")))

    title = listing_card.find('h3', class_="listivo-listing-card-name-selector").get_text().strip()
    description = listing_card.find('div', class_="listivo-listing-card-description-selector").get_text().strip()
    location = listing_card.find('div', class_="listivo-listing-card-address-selector").get_text().strip()
    price = listing_card.find('div', class_="listivo-listing-card-value-selector").get_text().strip()

    return {
      "title": title,
      "price": price,
      "description": description,
      "location": location,
      "link": listing_card["href"],
      # "images": list(map(parse_image_link, image_divs)) # This may or maynot be necessary
      **properties,
    }

  full_results = BeautifulSoup(api_result["template"], 'html.parser')
  listings_html = full_results.find_all('a', class_="listivo-listing-card-row-v2")
  return list(map(process_one_result, listings_html))


# Making API calls to the listivo api (this will be called using parameters from the chat app)

def get_listivo_listings(params):
  url = 'https://gojo.rent/wp-json/listivo/v1/listings'
  response = requests.post(url, data=format_params(params))
  if response.status_code == 200:
      data = process_results(response.json())
      return json.dumps(data)
  else:
      print('Error: Failed to retrieve data')
      return []
  