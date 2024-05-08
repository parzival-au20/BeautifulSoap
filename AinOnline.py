import requests
import json
import logging
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_ainonline_news():
    category = "Heli"
    web_site_name = "AinOnline"
    max_page = 4
    news_array = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    for page_number in range(max_page):
        url = f"https://www.ainonline.com/aviation-news/latest?page={page_number}"
        base_URL = f"https://www.ainonline.com"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            news_items = soup.select("a.Row_link__0_lcz")
            news_links = [item["href"] for item in news_items]
            
            try:
                for link in news_links:
                    link = base_URL + link
                    title, news_text, date, img_url = fetch_news_details(link, headers)
                    
                    if title and news_text and date and img_url and Content_Text_Control(date, news_text, web_site_name):
                        news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            except:
                print(f"Failed to fetch page: {link}")
                logging.info(f"Failed to fetch page: {link}")
        else:
            print(f"Failed to fetch page: {url} {response.reason} {response.status_code}")
            logging.info(f"Failed to fetch page: {url} {response.reason} {response.status_code}")
            return

    save_to_csv(news_array, web_site_name)

def fetch_news_details(link, headers):
    response = requests.get(link, headers = headers)
    title = None
    news_text = None
    date = None
    img_url = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        title_elem = soup.select_one(".Article_heading___vldJ")
        if title_elem:
            title = title_elem.text.strip()
        
        date_elem = soup.select_one(".BylineAndDate_date__dbokc")
        if date_elem:
            date = date_elem.text.strip()

        img_elem = soup.select_one(".MediaWithCaption_media__FPJ_M >img")
        if img_elem:
            img_url = img_elem["src"]
            
        next_data_script = soup.find("script", id="__NEXT_DATA__")
        script_content = next_data_script.string
        json_data = json.loads(script_content)
        try:
            text = json_data["props"]["pageProps"]["data"]["nodeById"]["fieldAinContentBody"][0]["entity"]["fieldAinComponent"][0]["entity"]["fieldText"]["processed"]
            soup = BeautifulSoup(text, "html.parser")
            news_text = soup.get_text()
        except:
            pass

    return title, news_text, date, img_url

