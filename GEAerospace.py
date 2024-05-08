import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_GEAerospace_news():
    base_url = "https://www.geaerospace.com/news/press-releases"
    base_URL = "https://www.geaerospace.com"
    category = "Heli"
    web_site_name = "GEAerospace"
    maxPage = 4
    news_array = []
    
    # User-Agent belirleyin, bazı sitelerde gerekli olabilir
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    for page_number in range(0, maxPage):
        try:
            response = requests.get(base_url+f"?page={page_number}", headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
            else:
                print(f"Failed to fetch page: {response.status_code} {response.status_code} {base_url}")
                return

            news_list = soup.select(".document-search-list > a")
            news_links = [link['href'] for link in news_list]
            
            for link in news_links:
                link = base_URL + link
                news_response = requests.get(link, headers=headers)
                if news_response.status_code != 200:
                    print(f"Error fetching news page {link}")
                    continue

                news_soup = BeautifulSoup(news_response.text, 'html.parser')

                title = news_soup.select_one(".press-banner-title").text.strip()
                news_text = news_soup.select_one(".paragraph > div").text.strip()
                about_ge_index = news_text.find("About GE Aerospace")
                if about_ge_index != -1:
                    news_text = news_text[:about_ge_index]
                date = news_soup.select_one(".press-banner-sub-title").text.strip()
                img_url = None  # Bu haber sitesinde haber resimleri yok.

                if Content_Text_Control(date, news_text, web_site_name):
                    news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
                else:
                    continue


        except Exception as e:
            print(f"An error occurred: {str(e)}")

    save_to_csv(news_array, web_site_name)
