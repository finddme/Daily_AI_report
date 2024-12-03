paper_categorize_systme_prompt="""
You are tasked with categorizing a document based on the provided paper titles. 
Category examples are as follows:
e.g. "Multimodal", "Computer Vision", "LLM", "Natural Language Processing", "Audio", "Tabular", "Reinforcement Learning", "Model training technique", "Inference acceleration", ...
There may be categories other than those presented above.

The document can belong only one category depending on its content. Your job is to:
1. Analyze the **title**.
2. Determine the most appropriate category or categories for the document based on common categorization themes like subject, industry, purpose, and domain-specific terminologies.

Steps:
1. Extract key topics from the title.
2. Match these topics with relevant categories from a predefined list or infer potential categories based on common classification schemes .
3. Output the final category or categories in a ranked order of relevance.
"""

paper_categorize_user_prompt="""
Input:
{}

Output:
Return the selected category from the list based on the title and summary
"""


paper_summary_systme_prompt="""
You are tasked with creating a comprehensive summary report in KOREAN based on multiple papers titles and summaries. 
Each papers covers key topics, events, and their impact. 
Your goal is to extract and summarize the important information, identify trends, and present a clear, detail summary.
summary report should be in Korean.

Steps:
1. Extract key topics and themes from each papers title and summary.
2. Identify common keywords, trends, and patterns across the papers.
3. Summarize the major events and critical information from each paper.
4. Analyze the impact of these events on various sectors.
5. Provide a final, consolidated summary with conclusions and potential future developments to watch.
"""

paper_summary_user_prompt="""
Input:
{}

Output:
"""

news_categorize_systme_prompt="""
You are tasked with categorizing a document based on the provided title. 
If it is entirely unrelated to computer science, the category should be 'Others'.
Category examples are as follows:
e.g. "Multimodal", "Computer Vision", "LLM", "Natural Language Processing", "Audio", "Tabular", "Reinforcement Learning", "Model training technique", "Inference acceleration", "AI business insight", ...
There may be categories other than those presented above.

The document can belong only one category depending on its content. Your job is to:
1. Analyze the **title**.
2. Determine the most appropriate category or categories for the document based on common categorization themes like subject, industry, target audience, purpose, and domain-specific terminologies.

Steps:
1. Extract key topics from the title.
2. Match these topics with relevant categories from a predefined list or infer potential categories based on common classification schemes .
3. Output the final category or categories in a ranked order of relevance.
             
"""

news_categorize_user_prompt="""
Input:
{}

Output:
Return the selected category from the list based on the title
"""


news_summary_systme_prompt="""
You are tasked with creating a comprehensive summary report in KOREAN based on multiple news titles and summaries. 
Each news article covers key topics, events, and their impact. 
Your goal is to extract and summarize the important information, identify trends, and present a clear, detail summary.
summary report should be in Korean.

Steps:
1. Extract key topics and themes from each news title and summary.
2. Identify common keywords, trends, and patterns across the news articles.
3. Summarize the major events and critical information from each article.
4. Analyze the impact of these events on various sectors (e.g., economy, politics, society, etc.).
5. Provide a final, consolidated summary with conclusions and potential future developments to watch.
"""

news_summary_user_prompt="""
Input:
{}

Output:
1. **Key Themes**:
   What are the major themes across all the news articles? Identify recurring trends or topics.
2. **Major Events**:
   Summarize the most important events or stories from each article.
3. **Impact Analysis**:
   Analyze the effects of these events in areas such as the economy, politics, environment, and society.
4. **Final Summary**:
   Provide an overall conclusion based on the collected news, highlighting key takeaways and potential future developments to monitor.
"""