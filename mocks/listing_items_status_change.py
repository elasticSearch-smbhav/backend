from enum import Enum
from mocks.random import generateRandomString
import random
from dotenv import load_dotenv
from AWS.sqs import publishToSqsQueue
import os

load_dotenv()

queueUrl = os.getenv("LISTINGS_ITEM_STATUS_CHANGE_QUEUE_URL")

class Status(Enum):
    BUYABLE = "BUYABLE"
    DISCOVERABLE = "DISCOVERABLE"
    DELETED = "DELETED"

class listingsItemStatusChange:
    def __init__(self, sellerId: str, sku: str, status: Status):
        self.sellerId = sellerId
        self.sku = sku
        self.status = status
        
    def __str__(self):
        return f"sellerId: {self.sellerId}, sku: {self.sku}, status: {self.status.name}"
    
    def __dict__(self):
        return {
            "SellerId": self.sellerId,
            "Sku": self.sku,
            "Status": self.status.name
        }
        
        
def generateRandomListingItemsStatusChange() -> listingsItemStatusChange:
    #all strings are 8 characters long
    sellerId = generateRandomString(8)
    sku = generateRandomString(8)
    
    #pick a random status
    status = random.choice(list(Status))
    
    return listingsItemStatusChange(sellerId, sku, status)

def publishListingItemsStatusChange(listingItemStatusChange: listingsItemStatusChange):
    response = publishToSqsQueue(queueUrl, listingItemStatusChange.__dict__())
    print(f"Published message to SQS queue: {response}")



    
    