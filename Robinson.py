import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_Robinson_news():
    base_url = "https://robinsonheli.com/press-releases-pr-robinson-press-releases/"
    category = "Heli"
    web_site_name = "Robinson"
    max_page = 1
    news_array = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    for page_number in range(max_page):
        url = base_url
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            news_items = soup.select(".blog-shortcode-post-title.entry-title > a")
            news_date_elems = soup.select(".fusion-date")
            news_month_year_elems = soup.select(".fusion-month-year")
            
            news_dates = [date.text.strip() + " " + year.text.strip() for date, year in zip(news_date_elems, news_month_year_elems)]
            
            for i, item in enumerate(news_items):
                link = item["href"]
                title = item.text.strip()
                news_text, img_url = fetch_news_details(link, headers)
                
                if news_text and Content_Text_Control(news_dates[i], news_text, web_site_name):
                    news_array.append([link, category, img_url, news_text, text_to_date(news_dates[i], web_site_name), title, web_site_name])
        else:
            print(f"Failed to fetch page: {response.status_code} {response.status_code} {url}")
            return

    save_to_csv(news_array, web_site_name)

def fetch_news_details(link, headers):
    response = requests.get(link,headers=headers)
    news_text = None
    img_url = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text_elements = soup.select(".fusion-text > p")
        news_text = "\n".join([p.text.strip() for p in text_elements])
        
        img_elem = soup.select_one(".attachment-full")
        if img_elem:
            img_url = img_elem["src"]

    return news_text, img_url

