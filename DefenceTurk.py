import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_DefenceTurk_news():
    category = "Heli"
    web_site_name = "DefenceTurk"
    maxPage = 7
    news_array = []

    for page_number in range(1, maxPage):
        page_url = f"https://www.defenceturk.net/haberler/page/{page_number}/"
        response = requests.get(page_url,)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
        else:
            print(f"Failed to fetch page: {response.status_code} {response.status_code} {page_url}")
            return
        
        news_list = soup.select(".jeg_post_title > a")

        news_links = [link["href"] for link in news_list]

        for link in news_links[:10]:
            response = requests.get(link,)
            if response.status_code != 200:
                print(f"Hata: {link} sayfasına erişilemedi")
                continue

            news_soup = BeautifulSoup(response.content, "html.parser")
            
            title = news_soup.select_one("h1.jeg_post_title").text.strip()
            news_text = news_soup.select_one(".wprt-container").text.strip()
            news_text = news_text.split("İlgili Olarak")[0]

            date_element = news_soup.select_one(".meta_left > .jeg_meta_date > a")
            if date_element:
                date = date_element.text.split("\n")[0]
            else:
                print(f"Hata: {link} sayfasındaki tarih bulunamadı")
                continue
            
            img_element = news_soup.select_one(".jeg_featured.featured_image > a > div > img")
            img_url = img_element["data-src"] if img_element else None

            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue
    
    save_to_csv(news_array, web_site_name)

