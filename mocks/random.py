import random
import string
import datetime

def generateRandomString(length=8, useSpecialChars=False):
    # Define the character sets
    charSet = string.ascii_letters + string.digits
    if useSpecialChars:
        charSet += string.punctuation  # Add special characters
    
    # Generate a random string
    randomString = ''.join(random.choice(charSet) for _ in range(length))
    
    return randomString


def generateRandomInt(min=0, max=100):
    return random.randint(min, max)


def generateRandomDateTime():
    # Generate a random date and time
    return datetime.datetime(
        random.randint(2000, 2020),
        random.randint(1, 12),
        random.randint(1, 28),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59)
    )


