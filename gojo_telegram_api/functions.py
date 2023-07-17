functions = [
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
                "bedrooms-from": {
                    "type": "number",
                    "description": "Defines the minimum number of bedrooms for filtering house rental listings."
                },
                "bedrooms-to": {
                    "type": "number",
                    "description": "Defines the maximum number of bedrooms for filtering house rental listings."
                },
                "bathrooms-from": {
                    "type": "number",
                    "description": "Defines the minimum number of bathrooms for filtering house rental listings."
                },
                "bathrooms-to": {
                    "type": "number",
                    "description": "Defines the maximum number of bathrooms for filtering house rental listings."
                },
                "land-size-from": {
                    "type": "number",
                    "description": "Defines the minimum land size in square meters for filtering house rental listings."
                },
                "land-size-to": {
                    "type": "number",
                    "description": "Defines the maximum land size in square meters for filtering house rental listings."
                },
                "property-size-from": {
                    "type": "number",
                    "description": "Defines the minimum property size in square meters for filtering house rental listings."
                },
                "property-size-to": {
                    "type": "number",
                    "description": "Defines the maximum property size in square meters for filtering house rental listings."
                },
                "pagination": {
                    "type": "number",
                    "description": "Specifies the page number of the search results for house rental listings."
                }
            }
        }
    }
]
