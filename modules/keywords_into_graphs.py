import os
from tkinter import messagebox
import glob
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from modules.read_csv_and_get_dict import *
from nltk.corpus import stopwords
from collections import  Counter

nlp_keyword_path = 'nlp_keywords'

new_stop_words =  ['COVID-19', 'coronavirus', 'Coronavirus', 'SARS-CoV-2', 'new', 'New', 'data',
                  'News', 'news', 'AP', 'number', 'numbers', 'cases', 'Cases', 'first', 'Update',
                  'Record', 'people', 'patients', 'Trump', '@realDonaldTrump', 'Health', 'health',
                  'use', 'Summary', 'summary', 'total', 'Total', 'Active', 'active' 'Today', 'today',
                  'disease']

sns.set_context("paper", rc={"font.size":8,"axes.titlesize":25,"axes.labelsize":27})  

def update_stop_words_with_keyword_permutations(keyword):
    keyword_split = keyword.split()
    if len(keyword) > len('Smoking Disorder'):
        for word in keyword_split:
            new_stop_words.extend(['@' + word.upper(),'@' + word.lower()])
            new_stop_words.extend(['#' + word.upper(),'#' + word.lower()])
            new_stop_words.extend([word.upper(),word.lower()])
            if word.find('-'):
                new_stop_words.extend([word.replace('-','').upper(),word.replace('-','').lower()])
                for sub_word in word.split('-'):
                    new_stop_words.extend([sub_word.upper(),sub_word.lower()])
    else:
        for word in keyword_split:
            new_stop_words.extend(list(map(''.join, itertools.product(*zip(('@' + word).upper(),('@' + word).lower())))))
            new_stop_words.extend(list(map(''.join, itertools.product(*zip(('#' + word).upper(),('#' + word).lower())))))
            new_stop_words.extend(list(map(''.join, itertools.product(*zip(word.upper(),word.lower())))))
            if word.find('-'):
                new_stop_words.extend(list(map(''.join, itertools.product(*zip(word.replace('-','').upper(),
                                                                        word.replace('-','').lower())))))
                for sub_word in word.split('-'):
                    new_stop_words.extend(list(map(''.join, itertools.product(*zip(sub_word.upper(),sub_word.lower())))))
    
# maximize_graph function code taken from https://stackoverflow.com/a/52324347
def maximize_graph(backend = None, fullscreen = False):
    """Maximize window independently on backend.
    Fullscreen sets fullscreen mode, that is same as maximized, but it doesn't have title bar (press key F to toggle full screen mode)."""
    if backend is None:
        backend = plt.get_backend()
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
            print ("Unrecognized backend: ", backend) #not tested on different backends (only Qt)
    plt.pause(0.1) #this is needed to make sure following processing gets applied (e.g. tight_layout)
    
def get_top_keywords_per_date_and_frequency(text_dict, keyword):
    x, y = [], []
    stop = set(stopwords.words('english'))
    stop.update(new_stop_words)
    for date, text in text_dict.items():
        if type(text) is not str:
            new = " ".join(text).split()
        else:
            new = text.split()
        most = Counter(new).most_common()
        word_count = 0
        count_total = 0
        concat_word = ''
        for word,count in most[:len(stop)+1]:
            if (word not in stop and word[0] != "@"):
                concat_word += (word + '\n')
                word_count += 1
                count_total += count
                if word_count == 3:
                    break
        concat_word += date
        x.append(count_total)
        y.append(concat_word)
    return x, y

def customize_keyword_graph(keyword_graph, file_name, keyword):
    keyword_graph.set_title(keyword.title() + ' ' + file_name[len(nlp_keyword_path)+1+len(keyword)+1+22:-len('_nlp_keywords.csv')]\
                             .replace('_', ' ').title() + ' Keyword Frequency over Time')
    keyword_graph.set_xlabel("Keywords, Date", fontsize = 15)
    keyword_graph.set_ylabel("Frequency")
    maximize_graph()
    keyword_graph.get_figure().savefig(file_name[:-len('.csv')] + '_graph.png', bbox_inches = 'tight')

def plot_histogram_top_non_stopwords(file_name, text_dict, keyword):
    x, y = get_top_keywords_per_date_and_frequency(text_dict, keyword)
    try:
        keyword_graph = sns.barplot(x = y, y = x)
    except ValueError:
        messagebox.showerror("Keyword Graph Error", "The " + keyword + " CSV file you are trying to graph is empty.")
    customize_keyword_graph(keyword_graph, file_name, keyword)
    plt.close('all')
    
def find_keyword_files(file_name):
    file_list = []
    for file in glob.glob(file_name):
        file_list.append(file)
    return file_list
    
def turn_keywords_into_graphs(keyword, start_date, end_date):
    update_stop_words_with_keyword_permutations(keyword)
    file_list = find_keyword_files(os.path.join(nlp_keyword_path, keyword + '_' + start_date + '_'\
                                                   + end_date + '_' + '*_nlp_keywords.csv'))
    if file_list:
        for file in file_list:
            keyword_dict = create_dictionary_object(open_read_csv_file(file))
            plot_histogram_top_non_stopwords(file, keyword_dict, keyword)
    else:
        return -1
    
def main():
    keyword = 'COVID-19'
    start_date = '11-10-2020'
    end_date = '12-11-2020'
    turn_keywords_into_graphs(keyword, start_date, end_date)
        
if __name__ == '__main__':
    main()
