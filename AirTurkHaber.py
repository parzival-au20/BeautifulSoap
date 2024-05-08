import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_AirTurk_news():
    category = "Heli"
    web_site_name = "AirTurkHaber"

    base_url = "https://www.airturkhaber.com/page/1/?s=helikopter"
    
    # User-Agent belirleyin, bazı sitelerde gerekli olabilir
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Failed to fetch page: {response.status_code} {response.status_code} {base_url}")
            return

        news_list = soup.select(".post-title.entry-title > a")
        news_links = [link['href'] for link in news_list]

        news_array = []
        for link in news_links:
            news_response = requests.get(link, headers=headers)
            if news_response.status_code != 200:
                print(f"Error fetching news page {link}")
                continue

            news_soup = BeautifulSoup(news_response.text, 'html.parser')

            title = news_soup.select_one(".post-title.entry-title > a").text.strip()
            text_elements = news_soup.select("div.entry-content > p")
            news_text = "".join([p.text.strip() for p in text_elements])
            date = news_soup.select_one(".date-container.minor-meta.updated").text.strip()

            img_url = None
            try:
                img_element = news_soup.select(".attachment-entry_with_sidebar")
                if img_element:
                    img_url = img_element[0]['src']
            except:
                pass

            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue

        save_to_csv(news_array, web_site_name)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

