from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd

# def init_browser():
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser("chrome", **executable_path, headless=False)


def scrape():

    # browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text
    
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    image_html = browser.html
    soup = BeautifulSoup(image_html, "html.parser")
    image_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov" + image_path

    marsweather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsweather_url)
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    facts_html = browser.html
    soup = BeautifulSoup(facts_html, 'html.parser')
    table_data = soup.find('table', class_="tablepress tablepress-id-mars")
    table_all = table_data.find_all('tr')
    labels = []
    values = []

    for tr in table_all:
        td_elements = tr.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)

        mars_facts_df = pd.DataFrame({
        "Label": labels,
        "Values": values
        })  

    fact_table = mars_facts_df.to_html(header = False, index = False)
    fact_table

    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    usgs_html = browser.html
    soup = BeautifulSoup(usgs_html, "html.parser")
    mars_hemisphere = []

    results = soup.find("div", class_ = "collapsible results" )
    hemispheres = results.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        img_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov" + img_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": fact_table,
        "hemisphere_images": mars_hemisphere
    }
    return mars_dict

if __name__ == "__main__":

 # If running as script, print scraped data
    print(scrape())