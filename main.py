from mocks.fulfillment_order_status import generateRandomFulfillmentOrderStatusNotification, publishFulfillmentOrderStatusNotification
from mocks.listing_items_mfn_quantity_change import generateRandomListingItemsMfnQuantityChange, publishListingItemsMfnQuantityChange
from mocks.listing_items_status_change import generateRandomListingItemsStatusChange, publishListingItemsStatusChange, Status, listingsItemStatusChange
from mocks.order import generateRandomOrder, publishOrderToQueue
from Mongo.order_access import OrderAccess
from Mongo.listing_access import ListingAccess
from AWS.kafka import createKafkaTopic
def main():
    # listingItemsMfnQuantityChange = generateRandomListingItemsMfnQuantityChange()
    # publishListingItemsMfnQuantityChange(listingItemsMfnQuantityChange)
    
    # fulfillmentOrderStatusNotification = generateRandomFulfillmentOrderStatusNotification()
    # publishFulfillmentOrderStatusNotification(fulfillmentOrderStatusNotification)
    
    # listingItemsStatusChange = listingsItemStatusChange("sellerId", "c91d6409f3862e68f6a4a71c3e0d6ec9", Status.BUYABLE)
    # publishListingItemsStatusChange(listingItemsStatusChange)
    
    # order = generateRandomOrder()
    # obj = OrderAccess()
    
    # print(obj.getAllOrders()[0].__dict__())
    # publishOrderToQueue(order)
    
    l = ListingAccess()
    
    print(l.getListing("c91d6409f3862e68f6a4a71c3e0d6ec9").__dict__())
    
if __name__ == "__main__":
    main()
