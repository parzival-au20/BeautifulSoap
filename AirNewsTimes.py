import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_AirNewsTimes_news():
    category = "Heli"
    web_site_name = "AirNewsTimes"
    news_array = []

    maxPage = 2
    for page_number in range(1, maxPage):
        url = f"https://www.airnewstimes.com/?s=helikopter&page={page_number}"
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
            continue

        news_list = soup.select("div > div > div > div > div > div > div > div > h3 > a")
        news_links = [link['href'] for link in news_list[9:27]]

        for link in news_links:
            try:
                response = requests.get(link)
                news_soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(f"Error fetching news page {link}: {e}")
                continue
            
            title = news_soup.select_one("article > div > div > div > div > div > div > div > div > h1").text.strip()
            text_elements = news_soup.select("article > div > div > div > div > div > div > div > div > div > div > div > div > p")
            news_text = ' '.join([p.text.strip() for p in text_elements])
            date = news_soup.select_one("div > time").text.strip()
            img_url = news_soup.select_one("div > div > div > div > div > img")['src'] if news_soup.select_one("div > div > div > div > div > img") else None

            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue
    
    save_to_csv(news_array, web_site_name)

