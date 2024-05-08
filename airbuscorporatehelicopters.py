import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_Airbus_news():
    base_url = "https://www.airbuscorporatehelicopters.com/website/en/ref/Press-Releases_319p2.html?noeu_id=319&lang=en"
    base_URL = "https://www.airbuscorporatehelicopters.com/website/en"
    base_img_URL = "https://www.airbuscorporatehelicopters.com/website"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    category = "Heli"
    web_site_name = "Airbus"
    news_array = []

    maxPage = 3
    for page_number in range(1,maxPage):
        try:
            response = requests.get(base_url+f"&page={page_number}", headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
            else:
                logging.error(f"Failed to fetch page: {response.status_code} {response.status_code} {base_URL}")
                return

            news_list = soup.select(".press-link > a.visible-xs")

            for news in news_list:
                link = news["href"]
                link = base_URL + link.split("..")[1]
                try:
                    response_article = requests.get(link, headers=headers)
                    soup_article = BeautifulSoup(response_article.content, "html.parser")
                    
                    title = soup_article.select_one("div > h1").text.strip()
                    news_text = soup_article.select_one("#press-body > div").text.strip()
                    date = soup_article.select_one("#press-date").text.strip().split("\n")[0]
                    img_url_element = soup_article.select_one(".img-paragraph > a > img")
                    img_url = base_img_URL + img_url_element["src"].split("..")[2] if img_url_element else None
                    if Content_Text_Control(date, news_text, web_site_name):
                        news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
                    else:
                        continue
                except Exception as e:
                    logging.error(f"Error processing article: {link}")
                    logging.error(e)
                    continue

        except Exception as e:
            logging.error(f"Error fetching news list: {base_url}")
            logging.error(e)
        
    save_to_csv(news_array, web_site_name)

