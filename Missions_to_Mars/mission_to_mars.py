#!/usr/bin/env python
# coding: utf-8

# In[9]:


# dependencies
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import pymongo


# ### NASA Mars News

# * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# In[2]:


executable_path = {'executable_path': 'chromedriver.exe'}


# In[14]:


def NasaMarsNews():
    url = 'https://mars.nasa.gov/news/?page=1&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('div', class_='bottom_gradient').text
    news = soup.find('div', class_='article_teaser_body').text
    browser.quit()
    return title, news


# In[15]:




# ### JPL Mars Space Images - Featured Image

# #Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
# 

# In[43]:


#src="www.jpl.nasa.gov/spaceimages/images/largesize/PIA24012_hires.jpg"
#url = 'https://photojournal.jpl.nasa.gov/jpegMod/PIA23896_modest.jpg'
import time
def MarsSpaceImages ():
    url = 'https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA23896'
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    relative_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = 'https://www.jpl.nasa.gov' + relative_path
    browser.quit()
    return(featured_image_url)    
    
        
    

    


# In[42]:




# ### Mars Weather
# 

# Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.

# In[45]:


def MarsWeather():
    url = 'https://twitter.com/marswxreport?lang=en'
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('div', class_="js-tweet-text-container")
    mars_weather = results.text
    browser.quit()

    return(mars_weather)






# ### Mars Facts
# 

# Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

# In[49]:


# def MarsFacts():
#     url = 'https://space-facts.com/mars/'
#     tables = pd.read_html(url)
#     df = tables[0]
#     df.columns = ['Characteristic Feather', 'Value']
#     df.set_index('Characteristic Feather', inplace=True)
#     df.index.names = ['']
#     return(df)

def MarsFacts():
    url="https://space-facts.com/mars/"
    browser=Browser("chrome", **executable_path, headless=False)
    browser.visit(url)
    fact_table=(pd.read_html(browser.html))
    fact_table=fact_table[0]
    fact_table.columns=['Characteristic Feather', 'Value']
    fact_table=fact_table.to_html(classes='marsinformation')
    fact_table=fact_table.replace('\n', ' ')    
    browser.quit()
   
    return (fact_table)


  


# In[50]:




# ### Mars Hemispheres
# 

# Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

# Cerberus Hemisphere

# In[112]:


#finding all of the URL

    


# In[117]:


def Mars_Hemispheres(url_list):
    base ='https://astrogeology.usgs.gov'
    browser = Browser('chrome', **executable_path, headless=True)
    hemisphere_image_urls = []
    for url in url_list:
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.text
        title = title.split('|')
        title = title[0]
        relative_path = soup.find('img', class_="wide-image")['src']
        image_url = base + relative_path
        image_dic = {"title":title, 
            "img_url":image_url}
        hemisphere_image_urls.append(image_dic)
    browser.quit()
    return(hemisphere_image_urls)


##Mars_Hemispheres(url_list)


# In[ ]:
# define a scrap function to call of the other function
def scrape():
    url_list = []
    base ='https://astrogeology.usgs.gov'
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_="item")
    for result in results:
        relative_url =  result.find('a')["href"]
        final_url = base + relative_url 
        url_list.append(final_url)
    title, Para = NasaMarsNews()
    results = {"title": title,
    "Paragraph" : Para,
    "Image": MarsSpaceImages(), 
    ##"weather":MarsWeather(), 
    "facts":MarsFacts(), 
    "hemispheres":Mars_Hemispheres(url_list)
    }
    return(results)



