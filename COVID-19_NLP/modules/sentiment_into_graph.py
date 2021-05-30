import os
import sys
sys.path.insert(0, 'backend processing')
import glob
import matplotlib.pyplot as plt
from read_csv_and_get_dict import *

path = 'nlp_sentiments'

#plt.set_context("paper", rc={"font.size":8,"axes.titlesize":25,"axes.labelsize":27})  
    
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

def customize_sentiment_graph(keyword):
    plt.gcf().autofmt_xdate()
    plt.title(keyword.title() + ' Health Pub and Tweet Sentiment over Time', fontsize = 25)
    plt.xlabel("Sentiment", fontsize = 20)
    plt.ylabel("Degree", fontsize = 20)
    plt.legend(loc="upper left")
    maximize_graph()
    plt.savefig(path + '\\' + keyword + '_sentiment_graph.png', bbox_inches = 'tight')
    plt.show()

def get_sentiment_per_date(sentiment_dict): 
    x1 = list(sentiment_dict)
    y1 = list(sentiment_dict.values())
    y1 = list(map(float, y1))
    return x1, y1

def plot_sentiment_linegraph(tweet_sentiment_dict, health_pub_sentiment_dict, keyword):
    x1, y1 = get_sentiment_per_date(tweet_sentiment_dict)
    x2, y2 = get_sentiment_per_date(health_pub_sentiment_dict)
    plt.plot(x1, y1, label = "Tweets")
    plt.plot(x2, y2, label = "Health Pub")
    customize_sentiment_graph(keyword)
    
def find_sentiment_files(file_name):
    file_list = []
    for file in glob.glob(file_name):
        file_list.append(file)
        print(file)
    return file_list  
    
def turn_sentiment_into_graph(keyword):
    file_list = find_sentiment_files(os.path.join(path, '*_nlp_sentiments.csv'))
    for file in file_list:
        if file[len(path)+1:-len('_nlp_sentiments.csv')] == 'health_pub':
            tweet_sentiment_dict = create_dictionary_object(open_read_csv_file(file))
        else: 
            health_pub_sentiment_dict = create_dictionary_object(open_read_csv_file(file))
    plot_sentiment_linegraph(tweet_sentiment_dict, health_pub_sentiment_dict, keyword)

def main():
    keyword = 'COVID-19'
    turn_sentiment_into_graph(keyword)
        
if __name__ == '__main__':
    main()
