from Mongo.listing_access import ListingAccess
from typing import List

# Initialize the MongoDB Listing Access object
listing_access = ListingAccess()

def check_inventory(query: str) -> dict:
    """
    Function to check inventory status using ListingAccess.
    """
    listing_id = query.strip()
    try:
        # Retrieve the listing details
        listing = listing_access.getListing(listing_id)
        
        # Convert Listing object to a dictionary
        listing_dict = listing.__dict__()

        # Remove 'Image Urls' if present
        listing_dict.pop("Image Urls", None)

        if 'Quantity' in listing_dict and 'Unique ID' in listing_dict:
            return {
                "status": "success",
                "message": f"{listing_dict['Quantity']} units of product {listing_dict['Unique ID']} are available in stock.",
                "data": listing_dict
            }
        else:
            return {
                "status": "error",
                "message": f"Listing data is missing required fields: {listing_dict}",
                "data": None
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching inventory data: {str(e)}",
            "data": None
        }

def get_listings_after_date(date: str) -> dict:
    """
    Function to fetch listings after a specific date.
    """
    try:
        listings = listing_access.getListingsAfterDate(date)
        if not listings:
            return {
                "status": "error",
                "message": f"No listings found after {date}.",
                "data": None
            }

        # Exclude 'Image Urls' from each listing's dictionary
        listings_data = [
            {key: value for key, value in listing.__dict__().items() if key != "Image Urls"}
            for listing in listings
        ]

        return {
            "status": "success",
            "message": f"Listings found after {date}",
            "data": listings_data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching listings after {date}: {str(e)}",
            "data": None
        }

def get_all_listings() -> dict:
    """
    Function to fetch all listings from the database.
    """
    try:
        listings = listing_access.getAllListings()
        if not listings:
            return {
                "status": "error",
                "message": "No listings found in the database.",
                "data": None
            }
        
        # Exclude 'Image Urls' from the listings data
        listings_data = [
            {key: value for key, value in listing.__dict__().items() if key != "Image Urls"} 
            for listing in listings
        ]
        
        return {
            "status": "success",
            "message": "All listings fetched successfully",
            "data": listings_data[0:5]  # Limit to the first 5 listings
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching all listings: {str(e)}",
            "data": None
        }
