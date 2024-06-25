import requests
from bs4 import BeautifulSoup

site_words = {
    "https://www.zhitomir.info": 'Житомир Інфо'
}

def checker():
    url = "https://www.zhitomir.info"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    news_item = soup.find("div", class_="news-item")
    site_name = site_words[url]

    news_date = news_item.find("div", class_="news-date").get_text()
    news_title = news_item.find("div", class_="news-title").get_text(strip=True)

    news_link = news_item.find("a", href=True)["href"]
    full_news_link = url + news_link

    news_response = requests.get(full_news_link)
    news_response.raise_for_status()

    news_soup = BeautifulSoup(news_response.content, "html.parser")
    first_paragraph = news_soup.find("p").get_text()
    
    return news_date, news_title, full_news_link, first_paragraph, site_name