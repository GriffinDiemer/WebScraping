import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def scrape():

    scraped_data = {}
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest" 

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")


    results = soup.find_all('div', class_="content_title")
    body_results = soup.find_all('div', class_="article_teaser_body")

    title = results[0].find('a').text
    body = body_results[0].text
    browser.quit()

    scraped_data['title'] =title
    scraped_data['body'] = body



    picture_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url = "https://www.jpl.nasa.gov"

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(picture_url)
    html = browser.html
    soup = bs(html, "html.parser")


    results = soup.find_all('article', class_='carousel_item')
    picture = results[0].a['data-fancybox-href']
    browser.quit()
    featured_image_url = url+picture
    scraped_data['featured_image'] = featured_image_url


    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(twitter_url)
    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    browser.quit()
    twitter_pic = results[0].find('a').text
    mars_weather = results[0].text
    mars_weather= mars_weather.replace('\n', '')
    mars_weather= mars_weather.replace(twitter_pic, '')
    scraped_data['mars_weather'] = mars_weather

    # site 4 - 
    facts_url = 'https://space-facts.com/mars/'
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(facts_url)
    html = browser.html
    soup = bs(html, "html.parser")

    facts_df = pd.read_html(facts_url)[0]
    browser.quit()
    scraped_data['facts'] = facts_df.to_html()

    html_file= open("facts_html.html","r")
    mars_facts = html_file.read()
    mars_facts.replace('\n', '')
    mars_facts = str(mars_facts)
    output_file = open('templates/cleaned_mars_facts.html', 'w+',encoding='utf8')
    output_file.write(mars_facts)
    output_file.close()
    html_file.close()
    #scraped_data['facts'] = facts_html

    # 5:


    mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(mars_url)

    html = browser.html
    soup = bs(html, "html.parser")

    names = []
    hemisphere_image = []
    base_url = 'https://astrogeology.usgs.gov'
    results = soup.find_all('h3')
    for result in results:
        planet_name = result.text
        names.append(planet_name)

    #This only worked with me telling soup that this is a new page. I am sure it isn't supposed to work this way. 
    #Was the loop what was messing it up? 
        
    for name in names:
        browser.visit(mars_url)
        time.sleep(1)
        browser.click_link_by_partial_text(name)
        html = browser.html
        soup = bs(html, "html.parser")
        time.sleep(1)
        pic = soup.find('img', class_='wide-image')
        hemisphere_image.append(pic)

    browser.quit()

    hemisphere_image[1]

    hemisphere_image_urls = []
    for picture in hemisphere_image:
        link = picture['src']
        full_link = base_url + link
        hemisphere_image_urls.append(full_link)

    joined_list = []
    for x in range(4):
        joined_list.append({"title":names[x],"img_url": hemisphere_image_urls[x]})

    scraped_data['joined_list'] = joined_list

    return scraped_data

if __name__ == "__main__":
    print(scrape())
