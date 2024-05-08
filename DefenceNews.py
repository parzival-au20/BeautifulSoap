import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_DefenceNews_news():
    base_url = "https://www.defensenews.com/search/helicopter"
    base_URL = "https://www.defensenews.com"
    category = "Heli"
    web_site_name = "DefenceNews"
    maxPage = 1
    news_array = []

    for page_number in range(1, maxPage + 1):
        page_url = base_url if page_number == 1 else f"{base_url}?page={page_number}"
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
        else:
            print(f"Failed to fetch page: {response.status_code} {response.status_code} {page_url}")
            return

        news_items = soup.select(".results-list--headline-container")
        news_dates = soup.select(".results-list--description-author-container > div > time")

        news_link = [item.find("a")["href"] for item in news_items]
        news_title = [item.text.strip() for item in news_items]
        news_date = [item.text.split("at")[0].strip() for item in news_dates]

        for link, title, date in zip(news_link, news_title, news_date):
            link = base_URL+link
            news_response = requests.get(link)
            if news_response.status_code != 200:
                print(f"Error fetching news article {link}")
                continue
            
            news_soup = BeautifulSoup(news_response.content, "html.parser")
            text_elements = news_soup.find_all("article")[0].find_all("p")
            news_text = "\n".join(p_text.text.strip() for p_text in text_elements)

            img_element = news_soup.select_one("section > div > div > div > figure > picture > img")
            img_url = img_element["src"] if img_element else None
            
            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue
    
    save_to_csv(news_array, web_site_name)

