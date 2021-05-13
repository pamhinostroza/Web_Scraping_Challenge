from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

# Create Mission to Mars Dictionary
mars_information = {}

def scrape_mars_news():
    browser = init_browser()

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    latest_news = soup.find('li', class_='slide')
    news_title = latest_news.find('div', class_='content_title').text
    news_paragraph = latest_news.find('div', class_='article_teaser_body').text

    browser.quit()
    return news_title, news_paragraph

def scrape_mars_image():
    browser = init_browser()

    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_img_url =  browser.find_by_xpath('/html/body/div[8]/div/div/div/div/img')["src"]

    featured_img_url

    browser.quit()

    return featured_img_url


def scrape_mars_facts():
    browser = init_browser()

    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_table_read = pd.read_html(mars_facts_url)
    mars_table = mars_table_read[0]
    mars_table = mars_table.rename(
        columns={0: "Keys", 1: "Values"}, errors="raise")
    mars_table.set_index("Keys", inplace=True)
    mars_table = mars_table.to_html()

    browser.quit()
    return mars_table



def mars_hemispheres():
    browser = init_browser()

    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    col_res = soup.find('div', class_ = 'collapsible results')
    usgs_items = col_res.find_all('div', class_ = 'item')
    usgs_list = []

    usgs_temp_url = 'https://astrogeology.usgs.gov'

    for item in usgs_items:
        try:
            hemisphere = item.find('div', class_ = 'description')
            title = hemisphere.h3.text
            hem_url = hemisphere.a['href']
            browser.visit(usgs_temp_url + hem_url)
            html = browser.html
            soup = bs(html, 'html.parser')
            usgs_images = soup.find('li').a['href']
            if (title and usgs_images):
                print('-' * 50)
                print(title)
                print(usgs_images)
# Use a Python dictionary to store the data using the keys `img_url` and `title`.
            usgs_dict = {
                'image_url': usgs_images,
                'title': title
            }
            usgs_list.append(usgs_dict)
        except Exception as e:
            print(e)

    browser.quit()
    return usgs_list