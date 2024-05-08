import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_AIAA_news():
    category = "Heli"
    web_site_name = "AIAA"
    news_array = []

    maxPage = 1
    for pagenumber in range(maxPage):
        url = "https://www.aiaa.org/news/press-releases"
        base_URL = "https://www.aiaa.org"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"Error fetching page {url} {response.reason} {response.status_code}")
                return
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
            continue

        news_list = soup.find_all(class_="item-list__thumbnail")
        news_links = [link['href'] for link in news_list]

        for link in news_links:
            try:
                response = requests.get(link,)
                news_soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(f"Error fetching news page {link}: {e}")
                continue
            
            title = news_soup.select_one(".page-title > span").text.strip()
            news_text = news_soup.select_one(".group.margin").text.strip()
            MediaContact_index = news_text.find("Media Contact")
            if MediaContact_index != -1:
                news_text = news_text[:MediaContact_index]
            try:
                date = news_soup.select_one(".page-title > small").text.replace("Written\n", "").strip()
            except Exception:
                print(f"{e} "+link)
            img_url = base_URL + news_soup.select_one("p strong img")['src'] if news_soup.select_one("p strong img") else None
            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue
    
    save_to_csv(news_array, web_site_name)


