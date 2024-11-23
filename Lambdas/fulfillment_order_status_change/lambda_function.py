from pymongo import MongoClient
import os
import json

class OrderAccess:
    _instance = None
    mongoUri = os.getenv("MONGO_URI")
    mongoDbName = os.getenv("MONGO_DB_NAME")
    orderCollectionName = os.getenv("ORDER_COLLECTION_NAME")
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create one
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):  # Check if already initialized
            self.client = MongoClient(OrderAccess.mongoUri)
            self.db = self.client[OrderAccess.mongoDbName]
            self.orderCollection = self.db[OrderAccess.orderCollectionName]
            self.initialized = True
            
    
    def updateOrderStatus(self, orderId: str, status: str):
        self.orderCollection.update_one({"OrderId": orderId}, {"$set": {"FulfillmentOrderStatus": status}})
        
        
orderAccess = OrderAccess()

def lambda_handler(event, context):
    
    for record in event['Records']:
        data = json.loads(record['body'])
        
        uniqueId = data['SellerFulfillmentOrderId']
        status = data['FilFillmentOrderStatus']
        
        orderAccess.updateOrderStatus(uniqueId, status)
        
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }