import pandas as pd

import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

def scraper():
    browser = Browser("chrome", executable_path="chromedriver", headless=False)
    snews_title, snews_p = mars_news(browser)
    return {
        "news_title": snews_title,
        "news_p": snews_p,
        "featured_image_url": mars_image(browser),
        "mars_weather": mars_twitter(browser),
        "mars_facts": mars_facts(),
        "mars_hemispheres": mars_hemisphere(browser)
    }

def mars_news(browser):
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html=browser.html
    soup = bs(html, "html.parser")
    listing_title = soup.find_all("div", {"class": "content_title"})
    len(listing_title)
    news_title = listing_title[0].find('a').get_text() #will grab top news title
    news_p = soup.find("div", class_="article_teaser_body").text
    return news_title, news_p


def mars_image(browser):

    images_url ="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)
    base_url="https://www.jpl.nasa.gov"
    browser.find_by_id('full_image').click()
    browser.is_element_present_by_text("more info", wait_time=5)
    more_info_element = browser.click_link_by_partial_text("more info")
    html=browser.html
    soup = bs(html, "html.parser")
    other_url = soup.find("img", class_="main_image")["src"]
    featured_url= base_url + other_url
    return featured_url


def mars_twitter(browser):
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    html=browser.html
    soup = bs(html, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    return mars_weather


def mars_facts():
    marsfacts_url = "https://space-facts.com/mars/"
    marsfacts = pd.read_html(marsfacts_url)
    mars_df = marsfacts[1]
    mars_df.columns=['Description', 'Value' ]
    mars_df.set_index('Description', inplace=True)
    return mars_df.to_html(classes = 'table table-striped')


def mars_hemisphere(browser):
    USGS_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(USGS_url)
    html=browser.html
    soup = bs(html, "html.parser")
    items = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    for i in items:     
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)
        partial_img_html = browser.html
        soup = bs( partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    return hemisphere_image_urls

