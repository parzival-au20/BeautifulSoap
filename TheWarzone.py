import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_TheWarzone_news():
    category = "Heli"
    web_site_name = "TheWarzone"
    base_URL = "https://www.twz.com"
    max_page = 3
    news_array = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
     
    for page_number in range(1, max_page):
        url = f"https://www.twz.com/category/air/page/{page_number}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            news_items = soup.select(".MuiTypography-root.MuiTypography-body1.css-o2o8wr")
            news_links = [item["href"] for item in news_items]

            for link in news_links:
                link = base_URL + link
                title, news_text, date, img_url = fetch_news_details(link,headers)
                
                if title and news_text and date and img_url and Content_Text_Control(date, news_text, web_site_name):
                    news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
        else:
            print(f"Failed to fetch page: {response.status_code} {response.status_code} {url}")
            return

    save_to_csv(news_array, web_site_name)

def fetch_news_details(link, headers):
    response = requests.get(link,headers=headers)
    title = None
    news_text = None
    date = None
    img_url = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        title_elem = soup.select_one(".MuiTypography-root.MuiTypography-h2.css-rvg3fn")
        if title_elem:
            title = title_elem.text.strip()
        
        news_text_elems = soup.select(".MuiTypography-root.MuiTypography-paragraph.paragraph > p")
        if news_text_elems:
            news_text = " ".join([elem.text.strip() for elem in news_text_elems])
        
        date_elem = soup.select_one(".css-1soycy3 > span > time")
        if date_elem:
            date_text = date_elem.text.strip()
            new_date = date_text.split(" ")
            date = " ".join(new_date[1:4])

        img_elem = soup.select_one(".MuiBox-root.css-1k6rbu > img")
        if img_elem:
            img_url = img_elem["src"]

    return title, news_text, date, img_url

