import requests
from bs4 import BeautifulSoup
import csv




# URL of the Amazon search results page
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"

#opening csv file
csvFile=open("amazon_products.csv",'w',newline="\n",encoding="utf-8")

#getting writer of csv file
csv_writer=csv.writer(csvFile)

#writing the row to csv file(header)
# csv_writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews','ASIN','Manufacturer','Item model number','Generic Name','Description'])


for page in range(1,21):
    #Making HTTP GET request for a page
    print("Scraping page:",page)
    response = requests.get(base_url+str(page))
    
    #parsing the data to simple text formate
    soup = BeautifulSoup(response.text, 'html.parser')
    
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for product in products:
        #selecting all <a> elemnts and retriving the url form it 
        product_url = "https://www.amazon.in"+product.find('a', {'class': 'a-link-normal'})['href']
        
        #selecting the span element and retriving the name of product
        product_name = product.find('span', {'class': 'a-text-normal'}).text
        product_price=0
        #retring the price of product
        product_price = product.find('span', {'class': 'a-price-whole'})
        if(product_price==None):
            product_price=0
        else:
            product_price=product_price.text
            
         
        #rating of product
        rating = product.find('span', {'class': 'a-icon-alt'}).text
        num_reviews = product.find('span', {'class': 'a-size-base'}).text if rating else 'N/A'
    
    
    
        csv_writer.writerow([product_url,product_name,product_price,rating,num_reviews])
        
        
#writing data ro csv file
print("data successfuly writen to csv file")

