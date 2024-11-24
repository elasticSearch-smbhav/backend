from inventory import check_inventory
print(check_inventory("c91d6409f3862e68f6a4a71c3e0d6ec9"))
from Mongo.listing_access import ListingAccess
print("-----------------------------------")
# Initialize the MongoDB Listing Access object
listing_access = ListingAccess()

listing = listing_access.getListing("c91d6409f3862e68f6a4a71c3e0d6ec9")
print(listing)