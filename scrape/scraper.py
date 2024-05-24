import requests
from bs4 import BeautifulSoup as bs 

class News:
    def __init__(self):
        self.aaj_tak_url="https://www.aajtak.in/"
        self.ndtv_url="https://www.ndtv.com/"
        self.data={"aaj_tak":[],"ndtv":[]}
    def scrape_aaj_tak(self):
        r=requests.get(self.aaj_tak_url).content
        soup=bs(r,"lxml")
        breaking_news=soup.find("div",class_="brack-text-rigt")
        breaking_news=breaking_news.find("a").get("href")
        r=requests.get(breaking_news).text
        def get_breaking(htm_pg):
            scraped_headlines=bs(htm_pg,"lxml")
            now=scraped_headlines.find("div",class_="breaking-news")
            now=now.find("h3").get_text()
            scraped_headlines=scraped_headlines.find_all("li")
            headlines=[]
            headlines.append(now)
            for i in scraped_headlines:
                try:
                    news=i.find('div',class_='content').find('p').get_text()
                    headlines.append(news)
                except Exception as e:
                    continue

            return headlines
        self.data["aaj_tak"].append({"breaking_news":get_breaking(r)})
        def get_news(url):
            r=requests.get(url).content
            content=bs(r,"lxml")
            news_container=content.find("div",class_="content-area")
            news_left=news_container.find("div",class_="left-story").find_all("a")
            news_left=[i.get("href") for i in news_left]
            news_mid=content.find("div",class_="sm-thumb-listing").find_all("a")
            news_mid=[i.get("href") for i in news_mid]
            news_right=content.find("div",class_="story-listing").find_all("a")
            news_right=[i.get("href") for i in news_right]
            def extract_news(link):
                news={}
                article=requests.get(link).content
                soup=bs(article,"lxml")
                soup=soup.find("div",class_="content-area")
                try:
                    news["heading"]=soup.find("div",class_="story-heading").get_text()
                    news["sub-heading"]=soup.find("div",class_="sab-head-tranlate-sec").get_text()
                    news["article"]=soup.find("div",class_="story-with-main-sec").find_all("p",class_="text-align-justify")
                    news["article"]=[i.get_text() for i in news["article"]]
                except Exception as e:
                    return {}
                return news
            news_left=[extract_news(i) for i in news_left]
            news_mid=[extract_news(i) for i in news_mid]
            news_right=[extract_news(i) for i in news_right]
            self.data["aaj_tak"].append({"major_news":news_left})
            self.data["aaj_tak"][-1]["major_news"].extend(news_mid)
            self.data["aaj_tak"][-1]["major_news"].extend(news_right)
        get_news(self.aaj_tak_url)
        x ={}
        x["Breaking_news"]=self.data["aaj_tak"][0]["breaking_news"]
        x["news"]=self.data["aaj_tak"][-1]["major_news"]
        return x

