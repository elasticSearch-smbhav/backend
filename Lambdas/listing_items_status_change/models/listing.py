from enum import Enum

class Status(Enum):
    BUYABLE = "BUYABLE"
    DISCOVERABLE = "DISCOVERABLE"
    DELETED = "DELETED"

class Listing:
    def __init__(self, uniqueId, date, timeStamp, siteName, category, productTitle, productDescription,
                 brand, packSizeOrQuantity, mrp, price, offers, comboOffers, stockAvailability, imageUrls, purchases, status=Status.DISCOVERABLE):
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

    def __dict__(self):
        """
        Returns the dictionary representation of the object.
        """
        return {
            "Unique ID": self.uniqueId,
            "Date": self.date,
            "Time Stamp": self.timeStamp,
            "Site Name": self.siteName,
            "Category": self.category,
            "Product Title": self.productTitle,
            "Product Description": self.productDescription,
            "Brand": self.brand,
            "Pack Size Or Quantity": self.packSizeOrQuantity,
            "Mrp": self.mrp,
            "Price": self.price,
            "Offers": self.offers,
            "Combo Offers": self.comboOffers,
            "Stock Availibility": self.stockAvailability,
            "Image Urls": self.imageUrls,
            "Purchases": self.purchases,
            "Status": self.status.name
        }

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        return f"Listing: {self.productTitle} ({self.category})\n" \
               f"Brand: {self.brand}\n" \
               f"Price: {self.price} (MRP: {self.mrp})\n" \
               f"Stock Availability: {self.stockAvailability}\n" \
               f"Date: {self.date} | Time: {self.timeStamp}\n" \
               f"Purchases: {self.purchases}\n" \
               f"Offers: {self.offers}\n" \
               f"Product Description: {self.productDescription}"

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
            status=status
        )
        
    