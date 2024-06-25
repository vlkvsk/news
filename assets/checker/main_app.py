import aiohttp
from bs4 import BeautifulSoup

from assets.data.db import add_post, change_m_id
from assets.handlers.handler_inline_all import send_post_to_confirm

async def fetch_news(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()

async def checker_zt():
    url = "https://www.zhitomir.info"
    async with aiohttp.ClientSession() as session:
        try:
            html = await fetch_news(session, url)
            soup = BeautifulSoup(html, "html.parser")
            news_item = soup.find("div", class_="news-item")
            news_title = news_item.find("div", class_="news-title").get_text(strip=True)
            news_link = news_item.find("a", href=True)["href"]
            full_news_link = url + news_link

            html_news = await fetch_news(session, full_news_link)
            news_soup = BeautifulSoup(html_news, "html.parser")
            first_paragraph = news_soup.find("p").get_text()

            if await add_post(post_id=0, post_title=news_title, post_link=full_news_link, post_text=first_paragraph, m_id=0):
                m_id = await send_post_to_confirm(p_title=news_title, p_link=full_news_link, p_text=first_paragraph, redak='Житомир Інфо')
                await change_m_id(m_id=m_id, title=news_title)
        except Exception as e:
            print(f"Error fetching Zhitomir news: {e}")

async def checker_tsn():
    url = "https://tsn.ua/news"
    async with aiohttp.ClientSession() as session:
        try:
            html = await fetch_news(session, url)
            soup = BeautifulSoup(html, "html.parser")
            news_item = soup.find("div", class_="l-col l-col--xs l-gap")
            if not news_item:
                return

            news_title = news_item.find("h3", class_="c-card__title").get_text(strip=True)
            news_link = news_item.find("a", class_="c-card__link")["href"]

            html_news = await fetch_news(session, news_link)
            news_soup = BeautifulSoup(html_news, "html.parser")

            data_content = news_soup.find("div", {"data-content": True})
            if data_content:
                paragraphs = data_content.find_all("p")[:2]
                news_content = "\n".join(p.get_text() for p in paragraphs)
            else:
                news_content = "Data content not found"

            if await add_post(post_id=0, post_title=news_title, post_link=news_link, post_text=news_content, m_id=0):
                m_id = await send_post_to_confirm(p_title=news_title, p_link=news_link, p_text=news_content, redak='ТСН')
                await change_m_id(m_id=m_id, title=news_title)
        except Exception as e:
            print(f"Error fetching TSN news: {e}")