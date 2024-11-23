import json
import os
from pymongo import MongoClient
from typing import List

class ListingAccess:
    mongoUri = os.getenv("MONGO_URI")
    mongoDbName = os.getenv("MONGO_DB_NAME")
    listingCollectionName = os.getenv("LISTING_COLLECTION_NAME")
    
    def __init__(self):
        self.client = MongoClient(ListingAccess.mongoUri)
        self.db = self.client[ListingAccess.mongoDbName]
        self.listingCollection = self.db[ListingAccess.listingCollectionName]
        
    
    def updateListingStatus(self, listingId: str, status: str):
        self.listingCollection.update_one({"Unique ID": listingId}, {"$set": {"Status": status}})

listingAccess = ListingAccess()

def lambda_handler(event, context):
    
    for record in event['Records']:
        data = json.loads(record['body'])
        
        uniqueId = data['Sku']
        status = data['Status']
        
        listingAccess.updateListingStatus(uniqueId, status)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }