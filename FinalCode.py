from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time


# -----------------------Product Class----------------------------------

class myData:
    productName= ""
    productType= ""
    actualPrice= 0
    soldQuantity = 0
    discountPrice = 0
    ratings = 0.0
    totalReviews = 0
    
    def __init__(self, productName, productType,actualPrice,soldQuantity,discountPrice,ratings,totalReviews):
        self.productName = productName
        self.productType = productType
        self.actualPrice = actualPrice
        self.soldQuantity = soldQuantity
        self.discountPrice = discountPrice
        self.ratings = ratings
        self.totalReviews = totalReviews



# ---------This function will return page content------------------------------ 

def getPageSourceByURL(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.refresh()
    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/2);")
    time.sleep(1)
    pageContent = driver.page_source
    soup = BeautifulSoup(pageContent, "html.parser")
    driver.quit()
    return soup






# ------------Global  Variables-------------------------------------------   
url = []
name = []
productsLinks = []
objectsList = []
pagesUrl = []





# -------This function will return categories List----------------------
def getCategoriesLinkFromMainPage():
    soup = getPageSourceByURL("https://www.daraz.pk/#")
    for link in soup.find_all('li',attrs={'class':'lzd-site-menu-sub-item'}):
        url.append(link.find('a')['href'])
        name.append(link.find('span').text)
    





# -------This function will return product links of given url---------
def getPoductsLinksFromCategoryPage(Url):
    soup = getPageSourceByURL(Url)
        
    for link in soup.find_all('div',attrs={'class':'title--wFj93'}):
        productsLinks.append(link.find('a')['href'])





# -------This function will return next page url---------------
def gotoNextPage(uRl,offset):
   Url = ""
   
   if (offset == 1):
     return "https:" + uRl + "?page=2"
   else:
       if(uRl[0] == 'h'):
           
           uRl = uRl.split("page=")
           Url = uRl[0] + "page=" + str(offset+1)
           
       else:
            uRl = uRl.split("page=")
            Url = "https:" + uRl[0] + "page=" + str(offset+5)
            
       return Url






# -------This function will scrap product and return product object and save in csv---------
def scrapProduct(url,category):
    soup = getPageSourceByURL(url)
    productName = (soup.find('span',attrs={'class':'pdp-mod-product-badge-title'}).text)
    totalReviews = (soup.find('a',attrs={'class':'pdp-link pdp-link_size_s pdp-link_theme_blue pdp-review-summary__link'}).text)
    discountedPrice = (soup.find('span',attrs={'class':'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'}).text)
    try:
        
        actualPrice = (soup.find('span',attrs={'class':'pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs'}).text)
    
    except:
        actualPrice = discountedPrice
    try:
        rating = (soup.find('span',attrs={'class':'score-average'}).text)
    except:
        rating = 0.0
    print(productName)
    totalReviews = totalReviews.split(" ")
    if(totalReviews[0] == 'No'):
        totalReviews = 0
    else:
        
        totalReviews = int(totalReviews[0])
    discountedPrice = discountedPrice.split(" ")
    discountedPrice = (discountedPrice[1])
    actualPrice = actualPrice.split(" ")
    actualPrice = (actualPrice[1])
    if(len(discountedPrice) > 3):
        discountedPrice = discountedPrice.split(",")
        discountedPrice = int(discountedPrice[0] + discountedPrice[1])
        
    if(len(actualPrice) > 3):
        actualPrice = actualPrice.split(",")
        actualPrice = int(actualPrice[0] + actualPrice[1])
            
    soldQuantity = totalReviews
    WriteIntoCsv(productName, category, actualPrice, soldQuantity, discountedPrice, rating, totalReviews)
    myProduct = myData(productName, category, actualPrice, soldQuantity, discountedPrice, rating, totalReviews)
    objectsList.append(myProduct)
# ----------This is the main Driver Function------------

def ScrapDataFromDaraz(n):
    start = 0
    getCategoriesLinkFromMainPage()
    for i in range (58,len(url)):
    
        getPoductsLinksFromCategoryPage("https:" + url[i])
        Link = url[i]
    
        for j in range(0,15):
        
        
            Link = gotoNextPage(Link,j+1)
            pagesUrl.append(Link)
            getPoductsLinksFromCategoryPage(Link)
    
        for k in range(start,len(productsLinks)):
            scrapProduct("https:"+ productsLinks[k], name[i])
        
        start = len(productsLinks)
def WriteIntoCsv(productName, category, actualPrice, soldQuantity, discountedPrice, rating, totalReviews):
    with open('data.csv', 'a',encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile,lineterminator='\n')
        writer.writerow([productName, category, actualPrice , discountedPrice , soldQuantity , rating , totalReviews]) 
 
        
 
# ------------------Function Calls---------------------
ScrapDataFromDaraz(10)  
 