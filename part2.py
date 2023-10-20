from bs4 import BeautifulSoup
import csv

from selenium import webdriver

#configuring webdriver
options = webdriver.EdgeOptions()
options.add_argument('headless')

# Set up the Edge WebDriver
driver = webdriver.Edge(options=options)


def get_names(l):
    res=""
    for val in l:
        if(val and val.isalnum()):
            res=res+" "+val
        elif(val and val[:-1].isalnum()):
            res=res+" "+val[:-1]
    return res



#scrap the product details from url and return a description and details
def getProductDetails(url):

    #scrapping raw data
    driver.get(url)

    # Parse the page with BeautifulSoup
    page_source = driver.page_source
    
    
    soup = BeautifulSoup(page_source, 'html.parser')
    
    #div which contains all product specifications
    product_features_div=soup.find("div",{'id':'detailBullets_feature_div'})
    features_name=None
    features_values=None
    if(product_features_div==None):
        product_features_table=soup.find("table",{'id':'productDetails_detailBullets_sections1'})
        if(product_features_table!=None):
            features_name=product_features_table.find('th')
            features_values=product_features_table.find("td")
        else:
            features_name=features_values=[]
    else:
        #names of features
        features_name=product_features_div.find_all("span",{'class':"a-text-bold"})

        #feature values
        features_values=product_features_div.select("span:not([class])")
    
    #product details div and ul
    product_description_div=None
    product_description_ul=None
    product_description_div=soup.find("div",{'data-a-expander-name':'productFactsDesktopExpander'})

    if(product_description_div==None):
        product_description_div=soup.find("div",{'id':'feature-bullets'})
        
    if(product_description_div!=None):
        #ul element    
        product_description_ul=product_description_div.find_all("ul",{'class':'a-unordered-list'})
        
            
    #for storing product details
    product_description_content=set()
    if(product_description_ul==None):
        product_description_content.add("N/A")
        product_description_ul=[]

    #scrapping actual product description and adding to set
    for ul in product_description_ul:
        value=ul.find('span',{'class':'a-list-item'}).text
        product_description_content.add(value)
    
    product_features={}
    product_features["ASIN"]="N/A"
    product_features["Manufacturer"]="N/A"
    product_features["Item model number"]='N/A'
    product_features["Generic Name"]="N/A"
    
    
    for x,y in zip(features_name,features_values):
        name,value=x.text.split(" "),y.text
        name=get_names(name).strip()
        if(name in requried):
            product_features[name]=value

    return ("**".join(product_description_content),product_features)




#requried features we need from product details
requried=set()
requried.add("ASIN")
requried.add("Manufacturer")
requried.add("Item model number")
requried.add("Generic Name")

csvFile=open("amazon_product_details.csv",'w',newline="\n",encoding="utf-8")

#getting writer of csv file
csv_writer=csv.writer(csvFile)

csv_writer.writerow(['ASIN', 'Manufacturer', 'Item model number', 'Generic Name','Description'])

with open('amazon_products.csv', 'r', newline='\n',encoding='utf-8') as file:
    data = list(csv.reader(file))
    
    for product in data:
        print(product[0])
        description, details=getProductDetails(product[0])
        csv_writer.writerow([details["ASIN"],details["Manufacturer"],details["Item model number"],details["Generic Name"],description])
    
# Close the browser

driver.quit()

