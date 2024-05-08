import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_VerticalMag_news():
    base_url = "https://verticalmag.com/news/"
    category = "Heli"
    web_site_name = "VerticalMag"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    maxPage = 3
    news_array = []

    for page_number in range(1, maxPage):
        page_url = base_url if page_number == 1 else f"{base_url}page/{page_number}/"
        response = requests.get(page_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
        else:
            print(f"Failed to fetch page: {response.status_code} {response.status_code} {page_url}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        news_list = soup.select("div.col-12 > a")

        for item in news_list[:12]:  # Sadece ilk 12 haber için
            link = item['href']
            news_page = requests.get(link, headers=headers)
            news_soup = BeautifulSoup(news_page.content, 'html.parser')

            try:
                title = news_soup.select_one("h1 > b > big").get_text(strip=True)
            except:
                print(link+" ERROR haberin title bulunamadı")
                continue

            try:
                text_elements = news_soup.select(".entry-content")
                news_text = "".join([p.get_text(strip=True) for p in text_elements])
            except:
                print(link+" ERROR haberin texti bulunamadı")
                continue

            try:
                date = news_soup.select_one(".author-title > .muted").get_text(strip=True)
            except:
                print(link+" ERROR haberin date bulunamadı")
                continue

            try:
                img_url = news_soup.select(".col-12 > .card > img")[0]['data-src']
            except:
                img_url = None

            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue

    save_to_csv(news_array, web_site_name)

