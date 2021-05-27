import glob
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from collections import  Counter

def plot_top_non_stopwords_barchart(fileName, text):
    stop=set(stopwords.words('english'))
    
    new= text.str.split()
    new=new.values.tolist()
    corpus=[word for i in new for word in i]

    counter=Counter(corpus)
    most=counter.most_common()
    x, y=[], []
    for word,count in most[:40]:
        if (word not in stop):
            x.append(word)
            y.append(count)

    ax = sns.barplot(x=y,y=x).set_title('COVID-19 Keyword Frequency over Time')
    plt.show()
    fig = ax.get_figure()
    print(fileName)
    fig.savefig(fileName[:-len('.csv')] + '_graph.png')

def find_keyword_files(file_name):
    file_list = []
    for file in glob.glob(file_name):
        file_list.append(file)
    return file_list  
    
def turn_keywords_into_graph():
    file_list = find_keyword_files('*_nlp_keywords.csv')
    for file in file_list:
        nlp_keyword_csv = pd.read_csv(file)
        nlp_keyword_csv.values.tolist()
       # for row in nlp_keyword_csv:
        plot_top_non_stopwords_barchart(file, nlp_keyword_csv['Keywords'])
    
def main():
    turn_keywords_into_graph()
        
if __name__ == '__main__':
    main()
