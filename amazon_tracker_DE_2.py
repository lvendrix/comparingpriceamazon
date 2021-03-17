import requests
from bs4 import BeautifulSoup
import validators

# We use a User Agent to make it look like a real request"
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}

# Infinite loop till user wants to stop
while True:
    # Getting the product's URL + checking if valid
    while True:
        URL = input("What's the URL of the Amazon product you ordered? ")
        valid=validators.url(URL)
        if valid==True:
            break
        else:
            print("Sorry, that does not look like a correct URL... Try again!")
            continue

    webpage = requests.get(URL, headers=HEADERS)

    # Creating a soup of information
    soup = BeautifulSoup(webpage.content, 'lxml')

    # Getting price of the product + checking if valid
    while True:
        try:
            purchase_price = float(input("What was its price? ").replace(",","."))
        except ValueError:
            print("Sorry, that does not look like a correct price. Try again!")
            continue
        else:
            break

    # Current price of the product
    def getPrice():
        # Price can be in different locations sometimes
        try:
            price = soup.find(id="price_inside_buybox").text
        except:
            price = soup.find(id="priceblock_ourprice").text
        
        #Cleaning the price
        price = price.strip()[1:].replace(",","")
        return price

    # Getting the name of the product and cleaning it
    title = ' '.join(soup.find("span", attrs={"id":'productTitle'}).text.strip().split()[:5])
        
    def trackPrice():
        # We need to convert the price to an INT to make calculations
        current_price = float(getPrice()) 
        # We only keep the first 5 words of the product's title to keep it clean
        diff = round(abs(purchase_price - current_price),2)
        percentage = round(diff/purchase_price*100,1)
        if current_price < purchase_price:
            print(f"The price of {title} is now {current_price} €, down by {diff} € (-{percentage}%) since you bought it. I am sorry my friend!")
        elif current_price > purchase_price:
            print(f"The price of {title} is now {current_price} €, up by {diff} € (+{percentage}%) since you bought it. You got a great deal!")
        else:
            print(f"The price of {title} has not changed so far.")

    if __name__ == "__main__":
        trackPrice()
    
    print()

    if (input('Do you want to track another product? [y/n] ')).lower() != 'y':
        print("Thank you for using this tracking tool!")
        break