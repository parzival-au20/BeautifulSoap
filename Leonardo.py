import time
import requests
from bs4 import BeautifulSoup
from convert_csv import save_to_csv, Content_Text_Control, text_to_date
import logging

def fetch_Leanardo_news():
    category = "Heli"
    web_site_name = "Leonardo"

    maxPage = 3
    news_array = []
    for page_number in range(1, maxPage):
        base_URL = "https://www.leonardo.com"
        url = f"https://www.leonardo.com/en/media-hub/news-stories?_com_leonardocompany_list_content_viewer_portlet_ListContentViewerPortlet_formDate=1673514460817&_com_leonardocompany_list_content_viewer_portlet_ListContentViewerPortlet_page={page_number}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
        else:
            print(f"Failed to fetch page: {response.status_code} {response.status_code} {base_URL}")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        news_list = soup.select("a.news-stories-card--wrap")
        
        news_link = []

        for item in news_list:
            href = item['href']
            news_link.append(href)

        for link in news_link:
            response = requests.get(link)
            if response.status_code != 200:
                print(f"Failed to fetch news article: {link}")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            try:
                title = soup.select_one("h1.hero-slide--content--title").get_text()
            except:
                print(f"Title not found for: {link}")
                continue
            
            try:
                news_text = soup.select_one(".check-html-content").get_text().strip()
            except:
                print(f"Text not found for: {link}")
                continue

            try:
                date = soup.select_one("div.hero-slide--content--description").get_text().strip()
            except:
                print(f"Date not found for: {link}")
                continue

            try:
                img_url = base_URL + soup.select(".hero-slide.slide1")[0]['data-img-url-d']
            except:
                img_url = None
                
            if(Content_Text_Control(date, news_text, web_site_name)):
                news_array.append([link, category, img_url, news_text, text_to_date(date, web_site_name), title, web_site_name])
            else:
                continue
    
    save_to_csv(news_array, web_site_name) 

