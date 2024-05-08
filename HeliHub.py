import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging
import re

def fetch_HeliHub_news():
    base_url = "https://helihub.com/tag/news/page/"
    category = "Heli"
    web_site_name = "HeliHub"
    maxPage = 3
    news_array = []

    for page_number in range(1, maxPage):
        url = f"{base_url}{page_number}/"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            news_list = soup.select(".newstxt > h2 > a")
            for news in news_list:
                link = news.get("href")
                title = news.get_text(strip=True)
                news_response = requests.get(link)
                if news_response.status_code == 200:
                    news_soup = BeautifulSoup(news_response.content, "html.parser")
                    news_text = news_soup.select_one(".editorial").get_text(strip=True)
                    date_text = news_soup.select_one(".newsdate").get_text(strip=True)
                    date = re.search(r'(\d+\-\w+\-\d+)', date_text).group(1)
                    img_url = None
                    try:
                        img_url = news_soup.select(".newsimg > img")[0].get("src")
                    except:
                        pass
                    if(Content_Text_Control(date, news_text, web_site_name)):
                        news_array.append([link, category, img_url, news_text, text_to_date(date,web_site_name), title, web_site_name])
                    else:
                        continue
                else:
                    print(f"ERROR: Unable to fetch news from {response.reason} {response.status_code} {link}")
        else:
            print(f"ERROR: Unable to fetch page {url}")
    
    save_to_csv(news_array,web_site_name)
