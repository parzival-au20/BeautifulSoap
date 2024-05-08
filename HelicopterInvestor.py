import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_HelicopterInvestor_news():
    url = "https://www.helicopterinvestor.com/news/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    category = "Heli"
    web_site_name = "HelicopterInvestor"
    news_array = []

    maxPage = 3
    for page_number in range(1,maxPage):
        try:
            response = requests.get(url+f"?_paged={page_number}", headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
            else:
                print(f"Failed to fetch page: {response.status_code} {response.status_code} {url}")
                logging.error(f"Failed to fetch page: {response.status_code} {response.status_code} {url}")
                return
            news_list = soup.select("article .articleExcerpt h3 a")

            for news in news_list[:20]:
                link = news["href"]
                try:
                    response_article = requests.get(link, headers=headers)
                    soup_article = BeautifulSoup(response_article.content, "html.parser")
                    
                    title = soup_article.select_one("article h1").text.strip()
                    paragraphs = soup_article.select("article p")
                    news_text = " ".join([p.text.strip() for p in paragraphs])
                    date = soup_article.select_one(".metaStrip time").text.strip()
                    img_url = soup_article.select_one(".featuredImage img")["data-src"] if soup_article.select_one(".featuredImage img") else None

                    if Content_Text_Control(date, news_text, web_site_name):
                        news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
                    else:
                        continue
                except Exception as e:
                    print(f"Error processing article: {link}")
                    logging.error(f"Error processing article: {link}")
                    print(e)
                    logging.error(e)
                    continue

        except Exception as e:
            print(f"Error fetching news list: {url}")
            logging.error(f"Error fetching news list: {url}")
            print(e)
            logging.error(e)
            return

    save_to_csv(news_array, web_site_name)