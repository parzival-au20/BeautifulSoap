import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_DefenceWeb_news():
    category = "Heli"
    web_site_name = "DefenceWeb"
    news_array = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

    maxPage = 1
    for page_number in range(maxPage):
        url = "https://www.defenceweb.co.za/category/aerospace/aerospace/"
            
        try:
            for i in range(20):
                response = requests.get(url, headers=headers)
                if response.status_code !=200:
                    print(url+" "+response.reason+" "+str(response.status_code))
                    continue
                else:
                    break
            if response.status_code !=200:
                print(response.reason+" "+str(response.status_code)+"  DefenceWeb scraping islemi BASARİSİZ" )
                return
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
            continue

        news_list = soup.find_all(class_="td-image-wrap")
        news_links = [link['href'] for link in news_list]

        for link in news_links:
            try:
                for i in range(10):
                    response = requests.get(link, headers=headers)
                    if response.status_code !=200:
                        print(response.reason+" "+str(response.status_code))
                        continue
                    else:
                        break
                if response.status_code !=200:
                    print(response.reason+" "+str(response.status_code)+link)
                    continue
                news_soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(f"Error fetching news page {link}: {e}")
                continue
            
            title = news_soup.select_one("h1.entry-title").text.strip()
            news_text = news_soup.select_one(".td-post-content").text.strip()
            date = news_soup.select_one(".td-post-date > time").text.strip().replace('th', '').replace('nd', '').replace('st', '').replace('rd', '')
            img_url = news_soup.select_one(".td-modal-image")['src'] if news_soup.select_one(".td-modal-image") else None

            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue
    
    save_to_csv(news_array, web_site_name)

