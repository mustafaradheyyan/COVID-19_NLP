import glob
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dlt
from read_csv_and_get_dict import *
from nltk.corpus import stopwords
from collections import  Counter

new_stop_words = ['COVID-19', 'covid-19', 'Covid-19', 'covid19', 'Covid19',
                  'COVID19', 'coronavirus', 'Coronavirus', 'SARS-CoV-2', 'new', 'New',
                  'use', 'number', 'numbers', 'cases', 'first', 'people', 'Trump',
                  'Update', '@realDonaldTrump', 'Record', 'Health', 'health',
                  'Summary', 'summary']

def plot_top_non_stopwords_barchart(file_name, text_dict, keyword):
    stop = set(stopwords.words('english'))
    stop.update(new_stop_words)
    
    x, y = [], []
    for date, text in text_dict.items():
        new = " ".join(text).split()
        most = Counter(new).most_common()
        
        for word,count in most[:len(stop)+1]:
            if (word not in stop):
                x.append(count)
                y.append(word + '\n' + date)
                break;
            
    sns.set_context("paper", rc={"font.size":8,"axes.titlesize":30,"axes.labelsize":30})  
    ax = sns.barplot(x = y, y = x)
    ax.set_title(keyword + ' ' + file_name[:-len('_nlp_keywords.csv')].replace('_', ' ').title() + ' Keyword Frequency over Time')
    ax.set_xlabel("Keyword\nDate", fontsize = 20)
    ax.set_ylabel("Frequency")#, fontsize = 30)
    #ax.tick_params('x', labelsize=8)
    plt.show()
    fig = ax.get_figure()
    fig.savefig(file_name[:-len('.csv')] + '_graph.png')

def find_keyword_files(file_name):
    file_list = []
    for file in glob.glob(file_name):
        file_list.append(file)
    return file_list  
    
def turn_keywords_into_graph(keyword):
    file_list = find_keyword_files('*_nlp_keywords.csv')
    for file in file_list:
        keyword_dict = create_dictionary_object(open_read_csv_file(file))
        plot_top_non_stopwords_barchart(file, keyword_dict, keyword)
    
def main():
    keyword = 'COVID-19'
    turn_keywords_into_graph(keyword)
        
if __name__ == '__main__':
    main()
