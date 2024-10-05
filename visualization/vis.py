import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import matplotlib.font_manager as fm
import os 
os.system('apt-get install fonts-nanum*')

def create_pie_chart_with_info(data,image_path):
    plt.rc('font', family='NanumSquare')
    
    plt.rcParams['axes.unicode_minus'] = False

    cluster_counts = Counter(item['category'] for item in data)
    
    # 클러스터 번호와 개수
    clusters = list(cluster_counts.keys())
    counts = list(cluster_counts.values())
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(clusters)))
    
    fig, (ax1) = plt.subplots(1, figsize=(8, 4), constrained_layout=True)
    
    ax1.pie(counts, labels=clusters, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Distribution')
    ax1.axis('equal')  
    
    cluster_info = {cluster: {'titles': [], 'categories': set()} for cluster in clusters}
    for item in data:
        cluster = item['category']
        cluster_info[cluster]['titles'].append(item['title'])
        cluster_info[cluster]['categories'].update(item['category'].split(', '))

    legend_labels = [f"========================================\n{cluster}: \n - " + "\n - ".join(cluster_info[cluster]['titles']) for cluster in clusters]
    ax1.legend(legend_labels, title="Graph Information", 
               loc="center left", 
               bbox_to_anchor=(1, 0, 0.5, 1)
                )

    
    plt.tight_layout()
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1) # subplot과의 간격 조정
    
    plt.savefig(image_path, bbox_inches='tight')
    
    # plt.show()

    # return plt
