import glob
import seaborn as sns
import pandas as pd
from read_csv_and_get_dict import *
import matplotlib.pyplot as plt
import matplotlib.dates as dlt

from nltk.corpus import stopwords
from collections import  Counter



def plot_top_non_stopwords_barchart(file_name, text_dict):
    stop=set(stopwords.words('english'))

    for date, text in text_dict.items():
        print(date)
        joined_dict_text = " "
        joined_dict_text = joined_dict_text.join(text)
        new = joined_dict_text.split()
        counter = Counter(new)
        most = counter.most_common()
        x, y = [], []
        #if (most[0] not in stop):
        #    x.append(most[0])
        #    y.append(date)
        for word,count in most[:40]:
            if (word not in stop):
                x.append(word)
                y.append(dlt.datestr2num(date))
                break;

    ax = sns.barplot(x = y, y = x).set_title('COVID-19 Keyword Frequency over Time')
    plt.show()
    fig = ax.get_figure()
    print(file_name)
    fig.savefig(file_name[:-len('.csv')] + '_graph.png')

def find_keyword_files(file_name):
    file_list = []
    for file in glob.glob(file_name):
        file_list.append(file)
    return file_list  
    
def turn_keywords_into_graph():
    file_list = find_keyword_files('*_nlp_keywords.csv')
    for file in file_list:
        keyword_dict = create_dictionary_object(open_read_csv_file(file))
        print(keyword_dict.keys())
        plot_top_non_stopwords_barchart(file, keyword_dict)
        keyword_dict = {}
    
def main():
    turn_keywords_into_graph()
        
if __name__ == '__main__':
    main()
