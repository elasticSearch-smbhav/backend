from pymongo import MongoClient
from typing import List
import os
import json

class ListingAccess:
    mongoUri = os.getenv("MONGO_URI")
    mongoDbName = os.getenv("MONGO_DB_NAME")
    listingCollectionName = os.getenv("LISTING_COLLECTION_NAME")
    
    
    def __init__(self):
        self.client = MongoClient(ListingAccess.mongoUri)
        self.db = self.client[ListingAccess.mongoDbName]
        self.listingCollection = self.db[ListingAccess.listingCollectionName]
    
    def updateQuantity(self, listingId: str, quantity: int):
        currentQuantity = self.listingCollection.find_one({"Unique ID": listingId})["Quantity"]
        
        newQuantity = currentQuantity - quantity
        
        if newQuantity < 0:
            newQuantity = 0
            
        self.listingCollection.update_one({"Unique ID": listingId}, {"$set": {"Quantity": newQuantity}})
        

listingAccess = ListingAccess()

def lambda_handler(event, context):
    
    for record in event['Records']:
        data = json.loads(record['body'])
        
        uniqueId = data['Sku']
        quantity = data['Quantity']
        
        listingAccess.updateQuantity(uniqueId, quantity)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }