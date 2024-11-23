from pymongo import MongoClient
from dotenv import load_dotenv
from mocks.order import Order
from typing import List
import os
from Mongo.listing_access import ListingAccess

load_dotenv()

listingAccess = ListingAccess()

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
        
    def insertOrder(self, order: Order):
        self.orderCollection.insert_one(order.__dict__())
        
    def close(self):
        self.client.close()
        
    def getOrder(self, orderId: str) -> Order:
        order = self.orderCollection.find_one({"OrderId":
                                                  orderId})
        
        return Order.__from_dict__(order)
    
    def updateOrder(self, order: Order):
        self.orderCollection.replace_one({"OrderId": order.orderId}, order.__dict__())
        
    def getOrdersAfterDate(self, date: str) -> List[Order]:
        orders = self.orderCollection.find({"PurchaseDate": {"$gt": date}})
        
        return [Order.__from_dict__(order) for order in orders]
    
    def getAllOrders(self) -> List[Order]:
        orders = self.orderCollection.find({})
        
        return [Order.__from_dict__(order) for order in orders]
    
    def getPrice(self, orderId: str) -> float:
        order = self.orderCollection.find_one({"OrderId":
                                                    orderId})
        
        price = 0
        
        for item in order["ListItems"]:
            price += listingAccess.getListing(item["SKU"]).price * item["Quantity"]
            
        return price
    
    def getPrices(self, listOrders: List[Order]) -> List[float]:
        return [self.getPrice(order.orderId) for order in listOrders]
    
    def updateOrderStatus(self, orderId: str, status: str):
        self.orderCollection.update_one({"OrderId": orderId}, {"$set": {"FulfillmentOrderStatus": status}})
    