from Mongo.listing_access import ListingAccess
# Initialize the MongoDB Listing Access object
listing_access = ListingAccess()

def check_inventory(query: str) -> str:
    """
    Function to check inventory status using ListingAccess.
    """
    # listing_id = query.split()[-1] 
    listing_id=query
    print(listing_id)
    try:
        # Retrieve the listing details
        listing = listing_access.getListing(listing_id)
        if listing:
            return f"{listing['quantity']} units of product {listing['uniqueId']} are available in stock."
        else:
            return f"Product with ID {listing_id} is not found in the inventory."
    except Exception as e:
        return f"Error fetching inventory data: {str(e)}"

print(check_inventory("c91d6409f3862e68f6a4a71c3e0d6ec9"))