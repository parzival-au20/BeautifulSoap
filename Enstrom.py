import requests
from bs4 import BeautifulSoup
import re
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_Enstrom_news():
    base_url = "https://enstromhelicopter.com/news/"
    category = "Heli"
    web_site_name = "Enstrom"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }

    maxPage = 3
    news_array = []
    for page_number in range(1, maxPage):
        page_url = base_url if page_number == 1 else f"{base_url}page/{page_number}"
        response = requests.get(page_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Failed to fetch page: {response.status_code} {response.status_code} {page_url}")
            return
        
        news_list = soup.select("div.blog-post-list > div.cell > h2 > a")
        news_link = [link['href'] for link in news_list]
        
        for link in news_link:
            response = requests.get(link, headers=headers)
            if response.status_code != 200:
                print(f"Error fetching news article {link}")
                continue
            
            article_soup = BeautifulSoup(response.text, 'html.parser')
            title = article_soup.find("h1", class_="blog-title").get_text(strip=True)
            text_elements = article_soup.select(".blog-post p")
            news_text = ' '.join([element.get_text(strip=True) for element in text_elements])
            date_text = article_soup.find(class_="byline").get_text(strip=True)
            date_match = re.search(r"\| (.+)$", date_text)
            date = date_match.group(1).strip() if date_match else None
            img_element = article_soup.find("div", class_="blog-post-feature-img").find("img")
            img_url = img_element['src'] if img_element else None

            if(Content_Text_Control(date, news_text, web_site_name)):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue

    save_to_csv(news_array, web_site_name)

