import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_airporthaber_news():
    category = "Heli"
    web_site_name = "AirportHaber"
    news_array = []

    url = "https://www.airporthaber.com/arama/?keyword=helikopter&cat=&p=1"
    base_url = "https://www.airporthaber.com"
    try:
        response = requests.get(url)
        if response.status_code ==200:
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Error fetching page {url} {response.reason} {response.status_code}")
            return
    except Exception as e:
        print(f"Error fetching page {url}: {e}")
        return

    news_list = soup.select(".news-item > a")
    news_img_list = soup.select(".news-item > a > img")

    news_links = [base_url+link['href'] for link in news_list]
    news_img_links = [base_url+img['src'] for img in news_img_list]

    for i, link in enumerate(news_links):
        try:
            response = requests.get(link)
            news_soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching news page {link}: {e}")
            continue

        title = news_soup.select_one(".news-title").text.strip()
        news_text = news_soup.select_one(".news-content").text.strip()
        date = news_soup.select_one(".news-date").text.strip()

        if Content_Text_Control(date, news_text, web_site_name):
            news_array.append([link, category, news_img_links[i], news_text, text_to_date(date, web_site_name), title, web_site_name])
        else:
            continue
    
    save_to_csv(news_array, web_site_name)


