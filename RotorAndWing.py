import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_RotorAndWing_news():
    base_url = "https://www.rotorandwing.com/news-archive/page/"
    category = "Heli"
    web_site_name = "RotorAndWing"
    max_page = 3
    news_array = []

    for page_number in range(1, max_page):
        url = f"{base_url}{page_number}/"
        response = requests.get(url,)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            news_items = soup.select(".article-info > h2 > a")
            news_img_elems = soup.select(".img-wrapper > a > img")
            
            news_links = [item["href"] for item in news_items]
            news_img_links = [img["src"] for img in news_img_elems]

            for link, img_url in zip(news_links, news_img_links):
                title, news_text, date = fetch_news_details(link)
                
                if title and news_text and date and Content_Text_Control(date, news_text, web_site_name):
                    news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
        else:
            print(f"Failed to fetch page: {response.status_code} {response.status_code} {url}")
            return

    save_to_csv(news_array, web_site_name)

def fetch_news_details(link):
    response = requests.get(link,)
    title = None
    news_text = None
    date = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        title_elem = soup.select_one(".post-header > h1")
        if title_elem:
            title = title_elem.text.strip()
        
        news_text_elem = soup.select_one(".the_content")
        if news_text_elem:
            news_text = news_text_elem.text.strip()
        
        date_elem = soup.select_one(".col-md-12 > p")
        if date_elem:
            date_text = date_elem.text.split("|")[1].strip()
            # Düzenleme
            date = date_text.split("\t")[0]

    return title, news_text, date

