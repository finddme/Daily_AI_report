import requests
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import pandas as pd
from urllib.parse import quote
import re
import arxiv
from datetime import datetime, timedelta


def get_deeplearn():
    print(f"--- get paper from deeplearn ---")
    base_url ="https://deeplearn.org"
    response = requests.get(base_url)
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    result=[]
    print(f"--- get paper from deeplearn : paper url crawling ---")
    for s in soup.find_all('div', class_='panel'):
        if s.find("h3", class_='panel-title').get_text(strip=True) == "Hot Papers":
            titles= soup.find_all('div', class_='title')
            for t in titles:
                url=base_url+t.find('a')['href']
                title=t.get_text(strip=True)
                result.append({"title":title,"url":url})
                
    final_res=[]
    print(f"--- get paper from deeplearn : paper page crawling ---")
    for idx,r in enumerate(result):
        if idx <=5:
            url=r["url"]
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                summary=soup.find("div",class_="article-content").find("p").get_text(strip=True)
                r["summary"]=summary
                final_res.append(r)
            except Exception as e:pass
    return final_res


def get_hf_daily():
    print(f"--- get paper from hf daily ---")
    today = datetime(2024, 9, 25)
    yesterday = today - timedelta(days=1)
    
    base_url=f"https://huggingface.co/papers?date="
    date=yesterday.strftime('%Y-%m-%d')
    url=base_url+date
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    arxiv_num=[]
    print(f"--- get paper from hf daily : arxiv number crawling ---")
    for idx,i in enumerate(soup.find_all("h3",class_='mb-1')):
        arxiv_num.append(i.find("a")["href"])
    
    result=[]
    print(f"--- get paper from hf daily : arxiv info crawling ---")
    for a_idx,an in enumerate(arxiv_num):
        if a_idx<=5:
            paper_id=an.strip("/papers/")
            search = arxiv.Search(id_list=[paper_id])
            paper = next(search.results())
            title=paper.title
            summary=paper.summary
            entry_id=paper.entry_id
            result.append({"title":title, "summary":summary, "url":entry_id})
    return result

def get_hot_papers():
    return get_deeplearn()+get_hf_daily()
