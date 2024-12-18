from pymongo import MongoClient
from dotenv import load_dotenv
from mocks.listing import Listing
import random
from typing import List
import os

load_dotenv()

class ListingAccess:
    _instance = None
    mongoUri = os.getenv("MONGO_URI")
    mongoDbName = os.getenv("MONGO_DB_NAME")
    listingCollectionName = os.getenv("LISTING_COLLECTION_NAME")
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create one
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):  # Check if already initialized
            self.client = MongoClient(ListingAccess.mongoUri)
            self.db = self.client[ListingAccess.mongoDbName]
            self.listingCollection = self.db[ListingAccess.listingCollectionName]
            self.initialized = True
        
        
    def insertListing(self, listing: Listing):
        self.listingCollection.insert_one(listing.__dict__())
        
    def close(self):
        self.client.close()
    
    
    def getListing(self, listingId: str) -> Listing:
        listing = self.listingCollection.find_one({"Unique ID":
                                                   listingId})
        
        return Listing.__from_dict__(listing)
    
    
    def updateListing(self, listing: Listing):
        self.listingCollection.replace_one({"Unique ID": listing.uniqueId}, listing.__dict__())
        
    def getListingsAfterDate(self, date: str) -> List[Listing]:
        listings = self.listingCollection.find({"Date": {"$gt": date}})
        
        return [Listing.__from_dict__(listing) for listing in listings]
    
    def getAllListings(self) -> List[Listing]:
        listings = self.listingCollection.find({})
        print(listings)
        return [Listing.__from_dict__(listing) for listing in listings]
    
    def updateListingStatus(self, listingId: str, status: str):
        self.listingCollection.update_one({"Unique ID": listingId}, {"$set": {"Status": status}})
        
        
    def updateQuantity(self, listingId: str, quantity: int):
        currentQuantity = self.listingCollection.find_one({"Unique ID": listingId})["Quantity"]
        
        newQuantity = currentQuantity - quantity
        
        if newQuantity < 0:
            newQuantity = 0
            
        self.listingCollection.update_one({"Unique ID": listingId}, {"$set": {"Quantity": newQuantity}})
        
    def getPaginated(self, pageNumber: int, pageSize: int) -> List[Listing]:
        listings = self.listingCollection.find({}).skip(pageNumber * pageSize).limit(pageSize)
        
        return [Listing.__from_dict__(listing) for listing in listings]
    
    
    
