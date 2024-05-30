from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup as bs 
from .models import News
from django.views.decorators.csrf import csrf_exempt
from pydantic import BaseModel
import subprocess
def translate(scentence):
    cmd=["translate-cli", "-t" ,"en", scentence]
    res=subprocess.check_output(cmd)
    res=res.split(":")[1].split("\n")[0]
    print(res)
    return res
class scrapeNews:
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
                    news["heading"]=soup.find('div',class_='story-heading').get_text()
                    try:
                        news["heading"]=translate(news["heading"].encode("utf-8"))
                    except Exception as e:
                        print(e)
                        pass
                    news["sub-heading"]=soup.find('div',class_='sab-head-tranlate-sec').get_text()
                    news["article"]=soup.find("div",class_="story-with-main-sec").find_all("p",class_="text-align-justify")
                    news["article"]=[i.get_text() for i in news["article"]]
                    
                except Exception as e:
                    return news
                entry=News(heading=news["heading"],subheading=news["sub-heading"],article=news["article"])
                entry.save()
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
    def scrape_ndtv(self):
        r=requests.get(self.ndtv_url).content
        soup=bs(r,"lxml")
        news1=soup.find("div",class_="vjl-row latest-stories-74").find_all("a")
        news2=soup.find("div",class_="vjl-row vjl-row-hf1 mb-10 top-stories-8").find_all("a")
        news3=soup.find("div",class_="vjl-row top-stories-8").find_all("a")
        news4=soup.find("div",class_="vjl-row mb-25 topscroll-17").find_all("a")
        news5=soup.find("ul",class_="Hrlst5_ul Hrlst5_num mb-10").find_all("a")
        news6=soup.find("div",class_="vjl-sm-12 vjl-md-12 vjl-lg-12 vjl-xl-6 res_ls-ns_rt entertainment-4437").find_all("a")
        news7=soup.find("div",class_="vjl-sm-12 vjl-md-12 vjl-lg-12 vjl-xl-6 res_ls-ns_lt Bqprime-4440").find_all("a")
        news8=soup.find("div",class_="FtSeoHp_txt-wr").find_all("a")
        news1.extend(news2)
        news1.extend(news3)
        news1.extend(news4)
        news1.extend(news5)
        news1.extend(news6)
        news1.extend(news7)
        news1.extend(news8)
        news=[i.get("href") for i in news1 ]
        for i in news:
            if "mp4" in i:
                news.pop(news.index(i))
            else:
                continue
        news=set(news)
        news=list(news)
        def extract_news(link):
            news={}
            db_save=News()
            r=requests.get(link).content
            soup=bs(r,"lxml")
            try:
                news["heading"]=soup.find('div',class_='sp-hd').find('h1').get_text()
                news["sub-heading"]=soup.find('div',class_='sp-hd').find('h2').get_text()
                news["article"]=[]
                news["article"].append(soup.find('div',class_='sp-cn ins_storybody').find('b').get_text())
                news["article"].extend([i.get_text() for i in soup.find("div",class_="sp-cn ins_storybody").find_all("p")])
            except Exception as e:
                return news
            entry=News(heading=news["heading"],subheading=news["sub-heading"],article=news["article"])
            entry.save()
            return news
        news=[extract_news(i) for i in news]
        return {"news":news}
class postnews(BaseModel):
    heading:str
    subheading:str
    article:str

def aajtak(request):
    a=scrapeNews()
    return JsonResponse(a.scrape_aaj_tak())
def ndtv(request):
    a=scrapeNews()
    return JsonResponse(a.scrape_ndtv())
@csrf_exempt
def post(request):
    import json
    if request.method=='POST':
        news=request.body.decode("utf-8")
        news=json.loads(news)
        entry=News(heading=news["heading"],subheading=news["subheading"],article=news["article"])
        entry.save()
        return JsonResponse({"status":"object created"})


