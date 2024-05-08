import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_MDHelicopters_news():
    base_url = "https://www.mdhelicopters.com/news/"
    category = "Heli"
    web_site_name = "MDHelicopters"
    max_page = 1
    news_array = []

    for page_number in range(max_page):
        url = base_url
        response = requests.get(url)
        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.content, "html.parser")
                news_items = soup.select("div.elementor > a")
                news_img_links = soup.select("div > picture.attachment-full.size-full > img")
                
                for i, item in enumerate(news_items[:6]):
                    link = item["href"]
                    title, news_text, date = fetch_news_details(link)
                    img_link = news_img_links[i]["data-lazy-src"] if i < len(news_img_links) else None
                    
                    if news_text and Content_Text_Control(date, news_text, web_site_name):
                        news_array.append([link, category, img_link, news_text, text_to_date(date,web_site_name), title, web_site_name])
            except  Exception as e:
                print(f"Hata oluştu: {e} {url}")
                return
        else:
            print(f"Failed to fetch page: {response.reason} {response.status_code} {url}")
            return

    save_to_csv(news_array, web_site_name)

def fetch_news_details(link):
    response = requests.get(link)
    title = None
    news_text = None
    date = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.select_one("h1.elementor-heading-title").text
        text_elements = soup.select("div.elementor-widget-theme-post-content > div > p")
        news_text = "\n".join([p.text.strip() for p in text_elements])
        
        date_elem = soup.select_one(".elementor-post-info__item--type-date")
        if date_elem:
            date = date_elem.text.strip()

    return title, news_text, date

