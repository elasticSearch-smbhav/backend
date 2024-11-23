from mocks.listing_items_status_change import Status
import math

class Listing:
    def __init__(self, uniqueId, date, timeStamp, siteName, category, productTitle, productDescription,
                 brand, packSizeOrQuantity, mrp, price, offers, comboOffers, stockAvailability, imageUrls, purchases, quantity, status=Status.DISCOVERABLE):
        self.uniqueId = uniqueId
        self.date = date
        self.timeStamp = timeStamp
        self.siteName = siteName
        self.category = category
        self.productTitle = productTitle
        self.productDescription = productDescription
        self.brand = brand
        self.packSizeOrQuantity = packSizeOrQuantity
        self.mrp = mrp
        self.price = price
        self.offers = offers
        self.comboOffers = comboOffers
        self.stockAvailability = stockAvailability
        self.imageUrls = imageUrls
        self.purchases = purchases
        self.status = status
        self.quantity = quantity
        

    def __dict__(self):
        """
        Returns the dictionary representation of the object.
        """
        
        #loop over fields and if any NaN values are
        #found, replace them with None
        
        
        #check for NaN in all the fields, cannot use __dict__
        
                
        def replace_nan(value):
            """ Helper function to replace NaN with None """
            if isinstance(value, (float, int)) and math.isnan(value):
                return ""
            return value

        # Return the object as a dictionary with NaN values replaced by None
        return {
            "Unique ID": replace_nan(self.uniqueId),
            "Date": replace_nan(self.date),
            "Time Stamp": replace_nan(self.timeStamp),
            "Site Name": replace_nan(self.siteName),
            "Category": replace_nan(self.category),
            "Product Title": replace_nan(self.productTitle),
            "Product Description": replace_nan(self.productDescription),
            "Brand": replace_nan(self.brand),
            "Pack Size Or Quantity": replace_nan(self.packSizeOrQuantity),
            "Mrp": replace_nan(self.mrp),
            "Price": replace_nan(self.price),
            "Offers": replace_nan(self.offers),
            "Combo Offers": replace_nan(self.comboOffers),
            "Stock Availability": replace_nan(self.stockAvailability),
            "Image Urls": replace_nan(self.imageUrls),
            "Purchases": replace_nan(self.purchases),
            "Status": replace_nan(self.status.name),  # Assuming status is not NaN, but handling for completeness
            "Quantity": replace_nan(self.quantity)
        }

    def __str__(self):
        """
        Returns a string representation of the object.
        Include unique id and status as well
        """
        
        return f"Listing: {self.productTitle} ({self.category})\n" \
                f"Brand: {self.brand}\n" \
                f"Price: {self.price} (MRP: {self.mrp})\n" \
                f"Stock Availability: {self.stockAvailability}\n" \
                f"Date: {self.date} | Time: {self.timeStamp}\n" \
                f"Purchases: {self.purchases}\n" \
                f"Offers: {self.offers}\n" \
                f"Product Description: {self.productDescription}\n" \
                f"Unique ID: {self.uniqueId}\n" \
                f"Status: {self.status.name}\n" \
                f"Quantity: {self.quantity}"

    @staticmethod
    def __from_dict__(data):
        """
        Static method that creates an instance of Listing from a dictionary.
        """
        # print(data)
        
        if data.get('Status') is not None:
            status = Status[data.get('Status')]
        else:
            status = Status.DISCOVERABLE
            
        if data.get('Quantity') is None:
            quantity = 0
        
        else:
            quantity = data.get('Quantity')
            
        return Listing(
            uniqueId=data.get('Unique ID'),
            date=data.get('Date'),
            timeStamp=data.get('Time Stamp'),
            siteName=data.get('Site Name'),
            category=data.get('Category'),
            productTitle=data.get('Product Title'),
            productDescription=data.get('Product Description'),
            brand=data.get('Brand'),
            packSizeOrQuantity=data.get('Pack Size Or Quantity'),
            mrp=data.get('Mrp'),
            price=data.get('Price'),
            offers=data.get('Offers'),
            comboOffers=data.get('Combo Offers'),
            stockAvailability=data.get('Stock Availibility'),
            imageUrls=data.get('Image Urls'),
            purchases=data.get('Purchases'),
            status=status,
            quantity=quantity
        )