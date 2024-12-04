import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.completion import Completion, Instructor
from get_information.paper import get_hot_papers
from get_information.news import get_hot_news
from model.prompt import *
from visualization.vis import create_pie_chart_with_info
from utils.formats import *
from utils.map import *
from utils.config import *
import json

class RUN:
    def __init__(self,args):
        self.args=args

        self.llm=llm_map[self.args.llm]

        # self.completion=Completion(self.llm)
        # self.instrctor=Instructor(self.llm)

        self.today = get_current_date_hyphen()

        self.result_path=f"./reports/{self.today}"
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)
        
        self.paper_image_path=f'{self.result_path}/paper_{self.today}.png'
        self.news_image_path=f'{self.result_path}/news_{self.today}.png'

    def summary(self, categorized_res, systme_prompt, user_prompt):
        category_dict = {}
        for item in categorized_res:
            category = item['category']
            category_dict.setdefault(category, []).append(item)

        summary_res=[]
        for cd_idx,(cd_k,cd_v) in enumerate(category_dict.items()):
            completion=Completion(self.llm)
            print(cd_idx)
            source=""
            insert_content=""
            for c in cd_v:
                title=c["title"]
                summary=c["summary"]
                url=c["url"]
                
                insert_content+=f"""
                - Title: '{title}'
                - Snippet/Abstract : '{summary}'
                """

                source+=f""" - {title} ({url})\n"""
            
            user_prompt_insert=user_prompt.format(insert_content)

            res=self.filtering_summary(completion,user_prompt_insert, systme_prompt)
            
            summary_res.append({"category":cd_k, 
                                # "summary":completion(user_prompt_insert, systme_prompt), 
                                "summary":res, 
                                "source":source})
        return summary_res
        
    def filtering_summary(self,completion,user_prompt_insert,systme_prompt,max_retries=5):
        retry_count = 0
        
        while retry_count < max_retries:
            result = completion(user_prompt_insert, systme_prompt)
            
            # 결과에 ", , , ,"가 포함되어 있는지 확인
            if ", , , ," in result:
                print(f"시도 {retry_count + 1}: 연속된 쉼표 발견. 재시도합니다.")
                retry_count += 1
                continue
            else:
                print("올바른 결과를 얻었습니다.")
                return result
        
        print(f"최대 재시도 횟수({max_retries})를 초과했습니다.")
        return result  # 마지막 시도의 결과를 반환
    
    def categorization(self, collected_info, systme_prompt, user_prompt):
        instrctor=Instructor(self.llm)
        print(f"--- categorization ---")
        titles=""
        for p_idx,pr in enumerate(collected_info):
            title=pr['title']
            titles+=f"{title} \n"

        user_prompt=user_prompt.format(titles)
   
        category=instrctor(user_prompt,
                            systme_prompt)
        print(category)
        categorized_res=[]  
        for c in category:
            for pr in collected_info:
                if c["title"] == pr["title"]:
                    if c["category"].lower() !="others" or c["category"].lower() !="none":
                        pr["category"]=c["category"]
                        categorized_res.append(pr)

        return categorized_res


    def paper(self):
        papers=get_hot_papers()

        categorized_res=self.categorization(papers,
                                        paper_categorize_systme_prompt,
                                        paper_categorize_user_prompt,
                                        )

        create_pie_chart_with_info(categorized_res,self.paper_image_path)

        print(f"--- paper summary ---")
        summary_res=self.summary(categorized_res,
                                paper_summary_systme_prompt,
                                paper_summary_user_prompt)

        return summary_res
    
    def news(self):
        news_infos=get_hot_news()
        categorized_res=[]
        while len(categorized_res) == 0:
            categorized_res=self.categorization(news_infos,
                                            news_categorize_systme_prompt,
                                            news_categorize_user_prompt,
                                            )

        create_pie_chart_with_info(categorized_res,self.news_image_path)

        print(f"--- news summary ---")
        summary_res=self.summary(categorized_res,
                                news_summary_systme_prompt,
                                news_summary_user_prompt)

        return summary_res

    def create_markdown_report(self,report_type,data,image_path=None):
        report = f"# Daily Artificial Intelligence Insights : {report_type}"

        if image_path:
            image_path=image_path.split("/")[-1]
            report += f"![Category Distribution Graph]({image_path})\n\n"

        for entry in data:
            category = entry.get('category', 'Unknown Category')
            summary = entry.get('summary', 'No summary provided')
            source = entry.get('source', 'No source provided')
            
            report += f"## {category}\n\n"
            
            report += f"**요약:**\n\n{summary}\n\n"
            
            report += f"**출처:**\n\n{source}\n\n"

        self.save_report_to_markdown(f'{self.result_path}/{report_type}_{self.today}_report.md', report)

        return report

    def save_report_to_markdown(self,filename, report_content):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)

    def report_generation(self):
        paper_summary_result=self.paper()
        news_summary_result=self.news()

        paper_md=self.create_markdown_report("Papers",
                                        paper_summary_result,
                                        self.paper_image_path)
        news_md=self.create_markdown_report("News",
                                        news_summary_result,
                                        self.news_image_path)
        # result=f"""# Daily Artificial Intelligence Insights \n\n{news_md} \n\n{paper_md}
        # """
        # self.save_report_to_markdown(f'{self.result_path}/{self.today}_report.md', result)

