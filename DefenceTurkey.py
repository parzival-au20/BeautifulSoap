import time
import requests
from bs4 import BeautifulSoup
import datetime
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_DefenceTurkey_news():
    category = "Heli"
    web_site_name = "DefenceTurkey"
    news_array = []

    maxPage = 2
    for page_number in range(1, maxPage):
        url = f"https://www.defenceturkey.com/tr/haberler/page/{page_number}/"
        try:
            response = requests.get(url)
            if response.status_code ==200:
                soup = BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"Error fetching page {url} {response.reason} {response.status_code}")
                return
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
            continue

        news_list = soup.select(".contentbox")
        news_links = [link['href'] for link in news_list]

        for link in news_links:
            try:
                response = requests.get(link)
                news_soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(f"Error fetching news page {link}: {e}")
                continue
            
            title = news_soup.select_one(".col-md-12 > .playfair").text.strip()
            text_elements = news_soup.select(".content > p")
            news_text = ' '.join([p.text.strip() for p in text_elements])
            date = news_soup.select_one(".col-md-12 > p").text.strip().split(" ")[1:4]
            date_str = " ".join(date).split("\n")[0]
            if date[0] == "Issue":
                date = datetime.datetime.now().strftime("%d %B, %Y")
            else:
                date = date_str

            img_url = news_soup.select_one(".item > a > img")['src'] if news_soup.select_one(".item > a > img") else None

            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue
    
    save_to_csv(news_array, web_site_name)

