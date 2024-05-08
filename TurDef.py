import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_TurDef_news():
    category = "Heli"
    web_site_name = "TurDef"
    maxPage = 3
    news_array = []

    for page_number in range(1, maxPage):
        url = f"https://turdef.com/news/air?page={page_number}"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error fetching page {url} {response.reason} {response.status_code}")
                return
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
            continue

        news_list = soup.select("div > div.post-content > h2 > a")
        news_links = [link['href'] for link in news_list]

        for link in news_links:
            try:
                response = requests.get(link)
                news_soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(f"Error fetching news page {link}: {e}")
                continue
            
            title = news_soup.select_one(".title-post > h1").text.strip()
            text_elements = news_soup.select(".post-content > p")
            news_text = ' '.join([p.text.strip() for p in text_elements])
            date_elements = news_soup.select("div.d-flex > ul.post-tags > li")
            date = date_elements[0].text.strip().split(',')[0]
            img_url = news_soup.select_one(".post-gallery > img")['src'] if news_soup.select_one(".post-gallery > img") else None

            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue
    
    save_to_csv(news_array, web_site_name)


