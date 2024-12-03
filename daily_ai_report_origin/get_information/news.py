import requests
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import pandas as pd
from urllib.parse import quote
import re

from datetime import datetime, timedelta


def get_hackernews():
    print(f"--- get news from hackernews ---")
    url ="https://hackernews.betacat.io/"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    titles=soup.find_all('div', class_='post-title') # get.text + href url
    metas=soup.find_all('div', class_='post-meta') # span : score 뽑기
    summaries=soup.find_all('div', class_='post-summary') # span : score 뽑기
    
    result=[]
    print(f"--- get news from hackernews : news summary crawling ---")
    for idx,(t,m,s) in enumerate(zip(titles,metas,summaries)):
        summary=s.get_text(strip=True)
        score=m.find("span",class_='score').get_text(strip=True)
        title=t.get_text(strip=True)
        url=t.find('a', class_='post-url')['href']
        result.append({"score":score, "title":title,"summary":summary,"url":url})
        
    sorted_result = sorted(result, key=lambda x: int(x['score']), reverse=True)
    
    hackernews=[]
    for sr in sorted_result:
        sr.pop("score")
        hackernews.append(sr)

    return hackernews
    
def get_mit_tech():
    print(f"--- get news from MIT tech ---")
    base_url ="https://www.technologyreview.kr/category/ai"
    response = requests.get(base_url)
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    result=[]
    print(f"--- get news from MIT tech : news summary crawling ---")
    for s in soup.find_all('div', class_='col-left'):
        try:
            title_section=s.find("h3",class_="entry-title")
            title=title_section.find("a").get_text(strip=True)
            post_url=title_section.find("a")["href"]
            summary=s.find("div", class_="post-excerpt").get_text(strip=True)
            result.append({"title":title,"summary":summary,"url":post_url})
    
        except Exception as e : pass
            
    return result[:5]

def get_hot_news():
    return get_mit_tech()+get_hackernews()
