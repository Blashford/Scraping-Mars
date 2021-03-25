import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time



def scrape():
    # Setting up the splinter browser
    executable_path = {"executable_path": "C:/Users/ashfo/Documents/bootcamp_homework/chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    # here we have the url we want to scrape then we use the browser to go to the site
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    # We use this sleep function after every .visit() to give the browser time to load the page
    time.sleep(1)
    # Then we capture the html and parse it
    html = browser.html
    soup = bs(html, "html.parser")
    # Then we go into the html to find the things we want
    li = soup.find("li", class_="slide")
    news_title = li.find("div", class_="content_title").text
    news_p = li.find("div", class_="article_teaser_body").text

    # Get the url, visit, sleep, and parse
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    # Here we grab the contents of a specific attribute, but it is only part of the full url needed for the image
    imagesoup = soup.find("div", page_score="1").a["href"]
    print(soup.find("div", page_score="1").a["href"])
    # So we have this base url to complete it and add them together then visit that url and sleep
    base_url = "https://www.jpl.nasa.gov"
    rel_url = base_url + imagesoup
    print(rel_url)
    browser.visit(rel_url)
    time.sleep(1)
    # Since we're on a new page now we have to grab and parse the html again
    html = browser.html
    soup = bs(html, "html.parser")
    # Then we find the path to the image that we want, which is also only a partial path so we have to add it to the base url
    featured_img_url = soup.find("img", class_="BaseImage")["src"]
     

    # Get url, visit, sleep, and parse
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    # Then we use a pandas function to read the table into a dataframe, then output it to html
    df = pd.read_html(url)[0]
    html_table = df.to_html(index = False, header = False)

    # Now we need to grab all of the hemispheres pictures so we get the url, visit, sleep, and parse
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    # Here we make an empty list to fill in our for loop
    hemisphere_img_urls = []
    # And we have our new base url to add all of our partial image urls to go to
    base_url = "https://astrogeology.usgs.gov"
    # Then we find our buttons that we need to click
    button = soup.find_all("div", class_="description")
    for link in button:
        # Here we initialize a dictionary so that it will be empty after each loop
        dicty = {}
        # And here we add the link text to the dictionary to we can label the picture
        dicty['title'] = link.a.text
        # Then we click on the link to go to the page with the image and sleep then parse
        browser.links.find_by_partial_text(link.a.text).click()
        time.sleep(1)
        html = browser.html
        img_soup = bs(html, "html.parser")
        # Here we need to find the image path in the html then we add the base url to it and add it to the dictionary
        rel_url = img_soup.find("img", class_="wide-image")["src"]
        dicty['img_url'] = base_url + rel_url
        # Then we add the dictionary to the list
        hemisphere_img_urls.append(dicty)
        # and then return to the original website and sleep
        browser.visit(url)
        time.sleep(1)

    # Then we quit the browser because we don't need it anymore
    browser.quit()

    # Then we add all the things we grabbed to a dictionary
    scrape_dicty = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img": featured_img_url,
        "table": html_table,
        "hemispheres": hemisphere_img_urls
    }

    # And we return the dictionary
    return scrape_dicty