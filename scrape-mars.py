import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

executable_path = {"executable_path": "C:/Users/ashfo/Documents/bootcamp_homework/chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    li = soup.find("li", class_="slide")
    news_title = li.find("div", class_="content_title").text
    news_p = li.find("div", class_="article_teaser_body").text


    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    imagesoup = soup.find("a", id="full_image")["data-link"]
    base_url = "https://www.jpl.nasa.gov"
    rel_url = base_url + imagesoup
    browser.visit(rel_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    img = soup.find("figure", class_="lede").a["href"]
    featured_img_url = base_url + img

    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    df = pd.read_html(url)[0]
    df[0] = [f'<b>{x}</b>' for x in df[0]]
    html_table = df.to_html(index = False, header = False)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    hemisphere_img_urls = []
    base_url = "https://astrogeology.usgs.gov"
    button = soup.find_all("div", class_="description")
    for link in button:
        dicty = {}
        dicty['title'] = link.a.text
        browser.links.find_by_partial_text(link.a.text).click()
        time.sleep(1)
        html = browser.html
        img_soup = bs(html, "html.parser")
        rel_url = img_soup.find("img", class_="wide-image")["src"]
        dicty['img_url'] = base_url + rel_url
        hemisphere_img_urls.append(dicty)
        browser.visit(url)
        time.sleep(1)