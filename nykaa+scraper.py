from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pandas as pd
record=[]
options = Options()
options.add_argument("user-data-dir=C:\\Users\\Alpha\\AppData\\Local\\Google\\Chrome\\User Data\\linkedin1")
bro = webdriver.Chrome(chrome_options=options)
print("ENTER THE FILENAME TO STORE LEADS")
file_name = input()
input()
pageCounter = 1
def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    moveBack = 0
    while True:
    #while count<1:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            moveBack = last_height
            break
        last_height = new_height
    driver.execute_script("window.scrollTo({}, {});".format(moveBack,moveBack-1080))
    driver.execute_script("window.scrollTo({}, {});".format(moveBack-1080,moveBack-(2*2080)))
        #count+=1
mainpageUrl = bro.current_url
mainpageUrl = mainpageUrl[0:-1]
with open("nykaa+temp+file.txt",'w') as file:
    while(pageCounter<=1):
        scroll(bro,2)
        ss=bro.page_source
        soup=BeautifulSoup(ss,'html.parser')
        listings = soup.findAll("div",{"class":"product-list-box card desktop-cart"})
        for i in listings:
            url = "https://www.nykaa.com"+i.find("a").get("href")
            file.write(url)
            file.write("\n")
            print(url)

        pageCounter+=1
        bro.get(mainpageUrl+str(pageCounter))
        time.sleep(2)

with open("nykaa+temp+file.txt",'r') as file:
    for line in file:
        bro.get(line)
        time.sleep(3)
        ss=bro.page_source
        soup=BeautifulSoup(ss,'html.parser')
        name = soup.find("h1",{"class":"product-title"}).text
        try:
            description = soup.find("div",{"class":"A-CellTxt"}).text
        except:
            description = ""
        try:
            avg_rating = soup.find("div",{"class":"m-content__product-list__ratings js-rating-count-popup"}).text[0]
        except:
            avg_rating = ""
        ratingsAndReviews = soup.find("div",{"class":"product-des__details-div scroll-to-target pull-left"}).text
        if("Rating" in ratingsAndReviews and "Review" in ratingsAndReviews):
            rating,review = ratingsAndReviews.split("\xa0&\xa0")
            totalrating = rating[0:rating.index(" ")]
            reviews = review[0:review.index(" ")]
            
        elif("Rating" in ratingsAndReviews):
            ratig = ratingsAndReviews
            totalrating = rating[0:rating.index(" ")]
            reviews = ""
        elif("Review" in ratingsAndReviews):
            review = ratingsAndReviews
            reviews = review[0:review.index(" ")]
            totalrating = ""

        try:
            price = soup.find("span",{"class":"mrp-price"}).text[1:]
            discount = soup.find("span",{"post-card__content-price-offer"}).text[1:]
        except:
            discount = ""
            price = soup.find("span",{"post-card__content-price-offer"}).text[1:]
            
        record.append((name,description,discount,price,avg_rating,totalrating,reviews))
        print(record)
        df=pd.DataFrame(record,columns=['Product Name','Product Brief Description','Discounted Price','Actual Price','Avg Review Score','No of Rating','No of Review'])
        df.to_csv(file_name + '.csv',index=False,encoding='utf-8')
        











        
        
        
