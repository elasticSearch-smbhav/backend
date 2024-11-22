from pymongo import MongoClient
from dotenv import load_dotenv
from mocks.listing import Listing
from typing import List
import os

load_dotenv()

class ListingAccess:
    mongoUri = os.getenv("MONGO_URI")
    mongoDbName = os.getenv("MONGO_DB_NAME")
    listingCollectionName = os.getenv("LISTING_COLLECTION_NAME")
    
    def __init__(self):
        self.client = MongoClient(ListingAccess.mongoUri)
        self.db = self.client[ListingAccess.mongoDbName]
        self.listingCollection = self.db[ListingAccess.listingCollectionName]
        
        
    def insertListing(self, listing: Listing):
        self.listingCollection.insert_one(listing.__dict__())
        
    def close(self):
        self.client.close()
    
    
    def getListing(self, listingId: str) -> Listing:
        listing = self.listingCollection.find_one({"uniqueId":
                                                   listingId})
        
        return Listing.__from_dict__(listing)
    
    
    def updateListing(self, listing: Listing):
        self.listingCollection.replace_one({"uniqueId": listing.uniqueId}, listing.__dict__())
        
    def getListingsAfterDate(self, date: str) -> List[Listing]:
        listings = self.listingCollection.find({"date": {"$gt": date}})
        
        return [Listing.__from_dict__(listing) for listing in listings]
    
    def getAllListings(self) -> List[Listing]:
        listings = self.listingCollection.find({})
        print(listings)
        return [Listing.__from_dict__(listing) for listing in listings]
    
