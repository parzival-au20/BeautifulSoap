import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_SavunmaSanayist_news():
    category = "Heli"
    web_site_name = "SavunmaSanayist"
    maxPage = 5
    news_array = []

    for page_number in range(1, maxPage):
        url = f"https://www.savunmasanayist.com/category/haberler/page/{page_number}/"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"Failed to fetch page: {url} {response.reason} {response.status_code}")
                return
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
            continue

        news_list = soup.select(".post-title > a")
        news_links = [link['href'] for link in news_list]

        for link in news_links:
            try:
                response = requests.get(link)
                news_soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(f"Error fetching news page {link}: {e}")
                continue
            
            title = news_soup.select_one("h1.post-title").text.strip()
            news_text = news_soup.select_one(".entry-content.entry").text.strip()
            date = news_soup.select_one("div.single-post-meta > span.date").text.strip()
            img_url = news_soup.select_one(".single-featured-image > img")['data-src'] if news_soup.select_one(".single-featured-image > img") else None

            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue
    
    save_to_csv(news_array, web_site_name)


