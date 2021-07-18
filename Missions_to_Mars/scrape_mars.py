# Dependencies
import time
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    # URL of Page to be Scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve the page
    browser.visit(url)

    # Wait Two Seconds to Load Page
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Examine Results, Determine Element That Contains Info
    news_titles = soup.find(class_='slide')

    # find News Title and Body
    news_title = news_titles.find(class_='content_title').text
    news_p = news_titles.find(class_="article_teaser_body").text

    # JPL Mars Space Images - Featured Image
    # URL of page to be scraped 
    url="https://www.jpl.nasa.gov/images?search=&category=Mars"

    # Retrieve the page
    browser.visit(url)

    # Wait Two Seconds to Load Page
    time.sleep(2)

    browser.links.find_by_partial_text('Image').click()
    # Wait Two Seconds to Load Page
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Examine Results, Determine Element That Contains Info
    featured_image_url = soup.find('img', class_="BaseImage")['src']

    # Mars Facts
    # Target URL
    url="https://space-facts.com/mars/"

    tables = pd.read_html(url)

    # Change Column Names
    df = tables[0]
    df = df.rename(columns={0: "Attributes", 1: "Mars_Values"})

    # add table content into a list of dictionaries
    mars_facts = df.to_dict('records')

    # Mars Hemispheres
    # URL Page to be Scraped 
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Retrieve Page
    browser.visit(url)

    # Wait Two Second to Load Page
    time.sleep(2)

    # Find Titles of the Images and Store in a List
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    titles=soup.find_all('h3')
    titles[:]=(title.text for title in titles)
    titles[:]=(title.split(" Enhanced")[0] for title in titles)
    hemisphere_image_urls=[]

    for title in titles:
        browser.visit(url)
        browser.links.find_by_partial_text(title).click()

        # Wait Two Seconds to Load Page
        time.sleep(2)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find Image URL
        img_url=soup.find('div',class_='downloads').ul.li.a['href']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    # Organized Scrpaed Data Into a Diction
    mars_data={"news_title":news_title, "news_p":news_p,"featured_image_url":featured_image_url,"mars_facts":mars_facts,
                "hemisphere_image_urls":hemisphere_image_urls}

    browser.quit()

    return mars_data

