import time
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_DefenseHere_news():
    category = "Heli"
    web_site_name = "DefenseHere"
    news_array = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        'Origin': 'https://www.defensehere.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://www.defensehere.com/tr/?s=helikopter&page=1'}
     
    maxPage = 2
    for page_number in range(1, maxPage):
        url = f"https://www.defensehere.com/tr/?s=helikopter&page={page_number}"
        try:
            for i in range(20):
                response = requests.get(url, headers=headers verify="./certificate/TUSAS_defenseHere.crt")
                req = Request(url=url, data=None, headers=headers)
                html = urlopen(req,context=ctx)
                html_read = html.read().decode('utf-8')
                bs4Obj=BeautifulSoup(html)
                time.sleep(10)
                if response.status_code !=200:
                    print(response.reason+" "+str(response.status_code))
                    continue
                else:
                    break
            if response.status_code !=200:
                print(response.reason+" "+str(response.status_code)+"  DefenceHere scraping islemi BASARİSİZ" )
                return
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
            return

        news_list = soup.select("article>div>header>h2>a")
        news_links = [link['href'] for link in news_list]

        for link in news_links:
            try:
                response = requests.get(link, verify="./certificate/TUSAS_defenseHere.crt")
                news_soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(f"Error fetching news page {link}: {e}")
                continue
            
            title = news_soup.select_one("article > div > header > h1").text.strip()
            news_text_elements = news_soup.select("article > div > div > p")
            news_text = "\n".join([element.text.strip() for element in news_text_elements])
            date = news_soup.select_one("article > div > div > span > time").text.split("-")[1].strip()
            img_url = news_soup.select_one("article > div > div > img")['src'] if news_soup.select_one("article > div > div > img") else None

            if Content_Text_Control(date, news_text, web_site_name):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue
    
    save_to_csv(news_array, web_site_name)

