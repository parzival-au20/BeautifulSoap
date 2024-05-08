import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_JustHelicopters_news():
    category = "Heli"
    web_site_name = "JustHelicopters"

    maxPage = 3
    news_array = []
    for page_number in range(1, maxPage):
        url = f"https://justhelicopters.com/Articles-and-News/Press-Releases?Page={page_number}"
        base_URL = f"https://justhelicopters.com"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
        else:
            print(f"Failed to fetch page: {response.status_code} {response.status_code} {url}")
            return

        news_list = soup.select("h1 > a")
        news_date_list = soup.select(".da_mark_back")
        
        news_link = []
        news_date = []

        for item, date in zip(news_list, news_date_list):
            href = item['href']
            news_link.append(href)
            date_obj = time.strptime(date.get_text(), "\n%b\n%d\n%Y\n")
            formatted_date = time.strftime("%d.%m.%Y", date_obj)
            news_date.append(formatted_date)

        for link, date in zip(news_link, news_date):
            response = requests.get(link)
            if response.status_code != 200:
                print(f"Failed to fetch news article: {link}")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            try:
                title = soup.select_one("h1").get_text()
            except:
                print(f"Title not found for: {link}")
                continue
            
            try:
                text_elements = soup.select(".da_body > p")
                news_text = "".join([p.get_text() for p in text_elements])

                READ_MORE_ROTOR_index = news_text.find("READ MORE ROTOR")
                if READ_MORE_ROTOR_index != -1:
                    news_text = news_text[:READ_MORE_ROTOR_index]
            except:
                print(f"Text not found for: {link}")
                continue

            try:
                img_url = base_URL+soup.select(".da_body > p > img")[0]['src']
            except:
                img_url = None

            if(Content_Text_Control(date, news_text, web_site_name)):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue
    
    save_to_csv(news_array, web_site_name) 

