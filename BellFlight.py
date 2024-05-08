import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_BellFlight_news():
    base_url = "https://news.bellflight.com"
    category = "Heli"
    web_site_name = "BellFlight"
    maxPage = 1
    news_array = []

    for page_number in range(1, maxPage + 1):
        page_url = f"{base_url}/en-US/page/{page_number}" if page_number > 1 else base_url
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            logging.error(f"Failed to fetch page: {response.status_code} {response.status_code} {page_url}")
            return
        news_list = soup.select(".img-wrap")
        BellPageNewsCount = 13

        for item in news_list[:BellPageNewsCount]:
            link = base_url+item["href"]
            news_response = requests.get(link,)
            if news_response.status_code != 200:
                logging.error(f"Error fetching news article {link}")
                continue

            news_soup = BeautifulSoup(news_response.text, "html.parser")
            title = news_soup.select_one(".heading-text > h2").text.strip()
            text_elements = news_soup.select(".text-hold")
            news_text = "\n".join(p_text.text.strip() for p_text in text_elements)
            date = news_soup.select_one(".heading-text > span time").text.strip().split(",")[0]
            img_url = news_soup.select_one(".img-wrap > img")["src"] if news_soup.select_one(".img-wrap > img") else None

            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
    
    save_to_csv(news_array, web_site_name)

