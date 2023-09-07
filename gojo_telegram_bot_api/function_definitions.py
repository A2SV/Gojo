function_definitions = [
    {
        "name": "get_listings",
        "description": "gets a list of house rental listings based on the parameters given",
        "parameters": {
            "type": "object",
            "properties": {
                "price-from": {
                    "type": "number",
                    "description": "Defines the minimum price for filtering house rental listings."
                },
                "price-to": {
                    "type": "number",
                    "description": "Defines the maximum price for filtering house rental listings."
                },
                "property-type": {
                    "type": "string",
                    "description": "Specifies the type of property for filtering house rental listings."
                },
                # "property-features": {
                #     "type": "array",
                #     "description": "An array of property feature strings for filtering house rental listings."
                # },
                "bathrooms-from": {
                    "type": "number",
                    "description": "Defines the minimum number of bathrooms for filtering house rental listings."
                },
                "bedrooms-from": {
                    "type": "number",
                    "description": "Defines the minimum number of bedrooms for filtering house rental listings."
                },
                "page": {
                    "type": "number",
                    "description": "Specifies the page number of the search results for house rental listings. It would be useful to load more results."
                }
            }
        }
    },
    {
        "name": "add_listing",
        "description": "Add a rental house listings based on the details given",
        "parameters": {
            "type": "object",
            "properties": {
                "landlord-name": {
                    "type": "string",
                    "description": "Defines the name of the person listing the property."
                },
                "landlord-contact": {
                    "type": "number",
                    "description": "Defines the contact information for the landlord listing the property."
                },
                "price": {
                    "type": "number",
                    "description": "Defines the monthly price for renting the property."
                },
                "property-type": {
                    "type": "string",
                    "description": "Specifies the type of property being listed (apartments, houses, service houses, and condominiums)."
                },
                "description": {
                    "type": "string",
                    "description": "Detailed context about a property to be listed that may not fit to specifics. This can include details about the area as well"
                },
                "title": {
                    "type": "string",
                    "description": "Display title about a property less than 50 characters"
                },
                "location": {
                    "type": "string",
                    "description": "The name of the location the property is at. This can be an area with a city"
                },
                "land-size": {
                    "type": "string",
                    "description": "Specifies the total area of land on the property (in ft squared)"
                },
                "property-size": {
                    "type": "string",
                    "description": "Specifies the total area of property within the land (in ft squared)"
                },

                # "property-features": {
                #     "type": "array",
                #     "description": "An array of property feature strings for the house rental listings."
                # },
                # "keywords": {
                #     "type": "array",
                #     "description": "Any keywords on the property to be searched with"
                # },
                "bathrooms": {
                    "type": "number",
                    "description": "Defines the number of bathrooms in the property"
                },
                "bedrooms": {
                    "type": "number",
                    "description": "Defines the number of bedrooms in the property"
                },
                "telegram-id": {
                    "type": "string",
                    "description": "Telegram Id of the user representing the session of communication"
                }
            }
        }
    }
]