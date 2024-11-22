from pymongo import MongoClient
from dotenv import load_dotenv
from mocks.order import Order
from typing import List
import os

load_dotenv()

class OrderAccess:
    mongoUri = os.getenv("MONGO_URI")
    mongoDbName = os.getenv("MONGO_DB_NAME")
    orderCollectionName = os.getenv("ORDER_COLLECTION_NAME")
    
    def __init__(self):
        self.client = MongoClient(OrderAccess.mongoUri)
        self.db = self.client[OrderAccess.mongoDbName]
        self.orderCollection = self.db[OrderAccess.orderCollectionName]
        
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
        
    