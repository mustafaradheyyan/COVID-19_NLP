import glob
import itertools
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dlt
from read_csv_and_get_dict import *
from nltk.corpus import stopwords
from collections import  Counter

new_stop_words = ['coronavirus', 'Coronavirus', 'SARS-CoV-2', 'new', 'New', 'use',
                  'number', 'numbers', 'cases', 'first', 'people', 'Trump', 'Update',
                  '@realDonaldTrump', 'Record', 'Health', 'health', 'Summary', 'summary']

sns.set_context("paper", rc={"font.size":8,"axes.titlesize":25,"axes.labelsize":27})  

def update_stop_words(keyword):
    new_stop_words.extend(list(map(''.join, itertools.product(*zip(keyword.upper(), keyword.lower())))))
    new_stop_words.extend(list(map(''.join, itertools.product(*zip(keyword.replace('-','').upper(),
                                                                keyword.replace('-','').lower())))))

# maximize_graph function code taken from https://stackoverflow.com/a/52324347
def maximize_graph(backend=None,fullscreen=False):
    """Maximize window independently on backend.
    Fullscreen sets fullscreen mode, that is same as maximized, but it doesn't have title bar (press key F to toggle full screen mode)."""
    if backend is None:
        backend=plt.get_backend()
    mng = plt.get_current_fig_manager()

    if fullscreen:
        mng.full_screen_toggle()
    else:
        if backend == 'wxAgg':
            mng.frame.Maximize(True)
        elif backend == 'Qt4Agg' or backend == 'Qt5Agg':
            mng.window.showMaximized()
        elif backend == 'TkAgg':
            mng.window.state('zoomed') #works fine on Windows!
        else:
            print ("Unrecognized backend: ",backend) #not tested on different backends (only Qt)

    plt.pause(0.1) #this is needed to make sure following processing gets applied (e.g. tight_layout)
    
def get_top_keywords_per_date_and_frequency(text_dict, keyword):
    x, y = [], []
    stop = set(stopwords.words('english'))
    stop.update(new_stop_words)
    for date, text in text_dict.items():
        new = " ".join(text).split()
        most = Counter(new).most_common()
        for word,count in most[:len(stop)+1]:
            if (word not in stop):
                x.append(count)
                y.append(word + '\n' + date)
                break;
    return x, y

def customize_keyword_graph(keyword_graph, file_name, keyword):
    keyword_graph.set_title(keyword + ' ' + file_name[:-len('_nlp_keywords.csv')]\
                             .replace('_', ' ').title() + ' Keyword Frequency over Time')
    keyword_graph.set_xlabel("Keyword\nDate", fontsize = 20)
    keyword_graph.set_ylabel("Frequency")
    maximize_graph()
    keyword_graph.get_figure().savefig(file_name[:-len('.csv')] + '_graph.png', bbox_inches = 'tight')

def plot_histogram_top_non_stopwords(file_name, text_dict, keyword):
    x, y = get_top_keywords_per_date_and_frequency(text_dict, keyword)
    keyword_graph = sns.barplot(x = y, y = x)
    customize_keyword_graph(keyword_graph, file_name, keyword)
    
def find_keyword_files(file_name):
    file_list = []
    for file in glob.glob(file_name):
        file_list.append(file)
    return file_list  
    
def turn_keywords_into_graph(keyword):
    update_stop_words(keyword)
    file_list = find_keyword_files('*_nlp_keywords.csv')
    for file in file_list:
        keyword_dict = create_dictionary_object(open_read_csv_file(file))
        plot_histogram_top_non_stopwords(file, keyword_dict, keyword)
    
def main():
    keyword = 'COVID-19'
    turn_keywords_into_graph(keyword)
        
if __name__ == '__main__':
    main()
