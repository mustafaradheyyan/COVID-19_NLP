import os
import glob
from datetime import datetime
import matplotlib.pyplot as plt
import modules.tweet_scraper as ts
import modules.read_csv_and_get_dict as rcsv

nlp_sentiments_path = 'nlp_sentiments' 
    
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

def add_horizontal_line(y, y_color, x):
    end_of_month_in_int = to_integer(datetime.strptime(ts.add_date_by_days(x, 15, '%m-%d-%Y'),'%m-%d-%Y'))
    beg_of_month_in_int = to_integer(datetime.strptime(ts.subtract_date_by_days(x, 15, '%m-%d-%Y'),'%m-%d-%Y'))
    plt.hlines(y, xmin=beg_of_month_in_int, xmax=end_of_month_in_int, color = y_color, linestyle = '-')

def add_horizontal_lines(y1, y1_color, y2, y2_color):
    plt.axhline(y1, color = y1_color, linestyle = '-')
    plt.axhline(y2, color = y2_color, linestyle = '-')

def adjust_y_axes_for_one_x_value(x1, x2, y1, y2):
    if len(x1) == 1 and len(x2) == 1:
        axes = plt.gca()
        axes.set_ylim([min(y1, y2) - 0.1, max(y1, y2) + 0.1])
        add_horizontal_lines(y1, 'blue', y2, 'orange')
    elif len(x1) == 1 and not len(x2) == 1:
        add_horizontal_line(y1, 'blue', x1[0])
    elif len(x2) == 1 and not len(x1) == 1:
        add_horizontal_line(y2, 'orange', x2[0])
        
def customize_sentiment_graph(keyword, bigger_x_int_axis, x1_date, x2_date, y1, y2, file_name):
    adjust_y_axes_for_one_x_value(x1_date, x2_date, y1, y2)
    plt.xticks(bigger_x_int_axis, x1_date if (len(x1_date) > len(x2_date)) else x2_date)
    plt.gcf().autofmt_xdate()
    plt.title(keyword.title() + ' Health Pub and Tweet Sentiment over Time', fontsize = 25)
    plt.xlabel("Date", fontsize = 20)
    plt.ylabel("Degree of Sentiment", fontsize = 20)
    plt.legend(loc="upper left")
    maximize_graph()
    plt.savefig(file_name[0:len(nlp_sentiments_path)+len('\\')+len(keyword)+1+22]\
                    + 'health_pub_tweet_' + file_name[-18:-4] + '_graph.png', bbox_inches = 'tight')

def to_integer(dt_time):
    return int(round(dt_time.timestamp() * 1000))

def get_sentiment_per_date(sentiment_dict): 
    x1 = list(sentiment_dict)
    x1 = [to_integer(datetime.strptime(value, '%m-%d-%Y')) for value in x1]
    y1 = list(sentiment_dict.values())
    y1 = list(map(float, y1))
    return x1, y1

def plot_sentiment_line_graph(tweet_sentiment_dict, health_pub_sentiment_dict, keyword, file_name):
    x1_date = list(tweet_sentiment_dict)
    x2_date = list(health_pub_sentiment_dict)
    x1_int, y1 = get_sentiment_per_date(tweet_sentiment_dict)
    x2_int, y2 = get_sentiment_per_date(health_pub_sentiment_dict)
    plt.plot(x1_int, y1, label = "Tweets")
    plt.plot(x2_int, y2, label = "Health Pub (Higher is more positive)")
    bigger_x_int_axis = x1_int if (len(x1_int) > len(x2_int)) else x2_int
    customize_sentiment_graph(keyword, bigger_x_int_axis, x1_date, x2_date, y1[0], y2[0], file_name)
    plt.close('all')
    
def find_sentiment_files(file_name):
    file_list = []
    for file in glob.glob(file_name):
        file_list.append(file)
    return file_list
    
def turn_sentiments_into_graph(keyword, start_date, end_date):
    file_list = find_sentiment_files(os.path.join(nlp_sentiments_path, keyword + '_' + start_date + '_'\
                                                   + end_date + '_' + '*_nlp_sentiments.csv'))
    if file_list:
        for file in file_list:
            if file[len(nlp_sentiments_path)+len('\\')+len(keyword)+len('_' + start_date + '_' + end_date):\
                                              -len('_nlp_sentiments.csv')] == '_health_pub':
                health_pub_sentiment_dict = rcsv.create_dictionary_object(rcsv.open_read_csv_file(file))
            else:
                tweet_sentiment_dict = rcsv.create_dictionary_object(rcsv.open_read_csv_file(file))
        plot_sentiment_line_graph(tweet_sentiment_dict, health_pub_sentiment_dict, keyword, file)
    else:
        return -1

def main():
    keyword = 'COVID-19'
    start_date = '11-10-2020'
    end_date = '12-11-2020'
    turn_sentiments_into_graph(keyword, start_date, end_date)
        
if __name__ == '__main__':
    main()