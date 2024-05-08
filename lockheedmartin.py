import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_lockheedmartin_news():
    base_url = "https://news.lockheedmartin.com/news-releases"
    category = "Heli"
    web_site_name = "lockheedmartin"
    max_page = 11
    news_array = []

    for page_number in range(0, max_page, 5):
        url = f"{base_url}?o={page_number}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            news_items = soup.select(".wd_title > a")
            news_date_list = soup.select(".wd_date")
            
            for item, date in zip(news_items,news_date_list):
                link = item["href"]
                title = item.text.strip()
                date = date.text.strip()
                news_text, img_url = fetch_news_details(link)
                
                if news_text and Content_Text_Control(date, news_text, web_site_name):
                    news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
        else:
            print(f"Failed to fetch page: {response.status_code} {response.status_code} {url}")
            return

    save_to_csv(news_array, web_site_name)

def fetch_news_details(link):
    base_URL = "https://news.lockheedmartin.com"
    response = requests.get(link)
    news_text = ""
    img_url = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        news_text_elem = soup.select(".wd_body.wd_news_body > p")
        if news_text_elem:
            for text_element in news_text_elem:
                news_text += text_element.text.strip()
            about_index = news_text.find("About Lockheed Martin")
            if about_index != -1:
                news_text = news_text[:about_index]
        

        img_elem = soup.select_one(".wd_asset_image > div > img")
        if img_elem:
            img_url = base_URL + img_elem["src"]

    return news_text, img_url

