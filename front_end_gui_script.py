from datetime import datetime
import modules.tweet_to_dict as t2d
import modules.generate_nlp_output as gnlp
import modules.process_nlp_output as pnlp
import modules.keywords_into_graphs as kgr
import modules.sentiments_into_graph as sgr
import modules.health_pub_scraper as hps
import modules.tweet_scraper as ts
import tkinter as tk

fields = 'Search Term', 'Start Date (mm-dd-yyyy)', 'End Date  (mm-dd-yyyy)',\
'Number of tweets per month', 'Number of health pubs per month','Number of keywords per nlp analysis',\
'IBM Watson NLU API Key','IBM Watson Service URL'
text_list = 'COVID-19', '01-12-2020', '05-24-2020', 1, 1, 2, 'ydoMxOX7J7I788-6Te0UO_YV9G7CO9az2tzkJlkegWcT',\
'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/69dbbfc3-ca34-4da9-986b-c5f0473ce007'

def error_check_keywords(number_of_keywords):
    if number_of_keywords <= 0:
        print_console_gui('Error! Number of keywords must be greater than 0\n', '\n', '\n')
        return 0
    else:
        return 1

def error_check_api_key_url(user_api_key, user_service_url):
    if gnlp.analyze_text_nlp(gnlp.nlu_authenticator(user_api_key, user_service_url), 'Testing testing 123', 1) == -1:
        print_console_gui('Error! Incorrect Watson NLU credentials.\n', '\n', '\n')
        return 0
    else:
        return 1

def error_check_date(start_date, end_date):
    try:
        if datetime.strptime(end_date, '%m-%d-%Y') <= datetime.strptime(start_date, '%m-%d-%Y'):
            print_console_gui('Error! End date should be after start date.\n', '\n', '\n')
            return 0
        else:
            if len(start_date) != 10 or len(end_date) != 10:
                print_console_gui('Error! Incorrect date format.\n', '\n', '\n')
            else:
                return 1
    except ValueError:
        print_console_gui('Error! Incorrect date format.\n', '\n', '\n')
        return 0

def error_check_per_month_value(tweets_per_month, pubs_per_month):
    if tweets_per_month <= 0:
        if pubs_per_month <= 0:
            print_console_gui('Error! Tweets and pubs per month should be greater than zero.\n', '\n', '\n')
            return 0
        else:
            print_console_gui('Error! Tweets per month should be greater than zero.\n', '\n', '\n')
            return 0
    elif pubs_per_month <= 0:
        print_console_gui('Error! Pubs per month should be greater than zero.\n', '\n', '\n')
        return 0
    else:
        return 1

def clean_search_text(search_term):
    return hps.re.sub('[^\w\-_\. ]', '_', search_term)

def fetch(entries):
    # Getting user input from text entries in GUI window, defaults are set above in [text_list]
    search_term = clean_search_text(entries[0][1].get())
    
    start_date = entries[1][1].get()
    end_date = entries[2][1].get()
    date_error_code = error_check_date(start_date, end_date)
    
    tweets_per_month = int(pnlp.is_number(entries[3][1].get()))
    pubs_per_month = int(pnlp.is_number(entries[4][1].get()))
    per_month_val_error_code = error_check_per_month_value(tweets_per_month, pubs_per_month)
    
    number_of_keywords = int(pnlp.is_number(entries[5][1].get()))
    keyword_error_code = error_check_keywords(number_of_keywords)
    
    user_api_key = entries[6][1].get()
    user_service_url = entries[7][1].get()
    api_error_code = error_check_api_key_url(user_api_key, user_service_url)
    
    if not all([keyword_error_code, api_error_code, date_error_code, per_month_val_error_code]):
        error_code = -1
    else:
        error_code = 1
    return search_term, start_date, end_date, pubs_per_month, tweets_per_month, number_of_keywords, user_api_key,\
                                                                                user_service_url, error_code

def start_processing(entries):
    search_term, start_date, end_date, pubs_per_month, tweets_per_month, number_of_keywords, user_api_key,\
              user_service_url, error_code = fetch(entries)
    if error_code == -1:
        return
    dict_of_urls, dict_of_text, error_code = web_scraping_for_keyword(search_term, start_date, end_date,\
    pubs_per_month, tweets_per_month)
    if error_code == -1: 
        return
    nlp_analysis_of_keyword_content(search_term, start_date, end_date, dict_of_urls, dict_of_text, user_api_key,\
                                                                            user_service_url, number_of_keywords)
    graph_functions(search_term, start_date, end_date)

def web_scraping_error_handling(start_date, end_date, search_term):
    if ts.check_tweet_availability(search_term, start_date, end_date):
        print_console_gui('Failure! 0 Results for term "' + search_term + '" and posted between "' +\
            start_date + '" and "' + end_date + '"\n\nSearch will now terminate!', '\n\n')
    else:
        print_console_gui('Failure! 0 tweet and health pub results for term "' + search_term + '" and posted between "' +\
            start_date + '" and "' + end_date + '"\n\nSearch will now terminate!', '\n\n')

def print_console_gui(text_output, new_line_gui, prefix_new_line_console=''):
    print(prefix_new_line_console + text_output, flush = True)
    text.insert(tk.END, text_output + new_line_gui)

def web_scraping_for_keyword(search_term, start_date, end_date, pubs_per_month, tweets_per_month):
    # Reading health pub csv file and creating dictionary object
    print_console_gui('\nScraping medRxiv "' + search_term + '" publication urls', '\n')
    dict_of_urls, error_code = hps.health_pub_scraper(pubs_per_month, start_date, end_date, search_term)
    if error_code == -1:
        web_scraping_error_handling(start_date, end_date, search_term)
        return None, None, error_code
    # Getting English tweets from Twitter based on dates and search term
    else:
        print_console_gui('Success\n\nScraping Twitter tweets', '\n')
    error_code = ts.tweet_scraper(tweets_per_month, start_date, end_date, search_term)
    if error_code == -1:
        print_console_gui('Failure! 0 Results for term "' + search_term + '" and posted between "' +\
        start_date + '" and "' + end_date + '"\n\nSearch will now terminate!', '\n\n')
        return None, None, error_code
    # Reading tweets csv files and creating a dictionary object from it
    print_console_gui('Success\n\nConverting tweet csv files into a text dictionary', '\n')
    dict_of_text = t2d.get_tweet_csv_data_into_text_dict(start_date, end_date, search_term)
    return dict_of_urls, dict_of_text, 1

def nlp_analysis_of_keyword_content(search_term, start_date, end_date, dict_of_urls, dict_of_text, user_api_key, user_service_url, number_of_keywords):
    # Processing dictionary object with NLP to return a keywords and sentiments file
    # The 'health_pub' part of the string signifies the NLP file name and the ".url" is the NLP query type
    print_console_gui('Success\n\nProcessing health pub urls with NLP', '\n')
    file_name_prefix = search_term + '_' + start_date + '_' + end_date + '_health_pub'
    pnlp.get_nlp_keywords_and_sentiment_to_file(file_name_prefix, dict_of_urls, 'url', user_api_key, user_service_url, number_of_keywords)
    # Processing dictionary object with NLP to return a keywords and sentiments file
    # The 'tweet' part of the string signifies the NLP file name and the "text" is the NLP query type
    print_console_gui('Success\n\nProcessing tweets with NLP', '\n')
    file_name_prefix = search_term + '_' + start_date + '_' + end_date + '_tweet'
    pnlp.get_nlp_keywords_and_sentiment_to_file(file_name_prefix, dict_of_text, 'text', user_api_key, user_service_url, number_of_keywords)
    print_console_gui('Success!', '\n\n')

def graph_functions(search_term, start_date, end_date):
    # Turning (both) NLP keyword csv files into histogram graphs with the top keyword per month
    print_console_gui('Processing NLP keyword csv files into graphs', '\n', '\n')
    error_code = kgr.turn_keywords_into_graphs(search_term, start_date, end_date)
    if error_code == -1:
        print_console_gui('Failure :( Keyword csv files not found\n', '\n')
    else:
        print_console_gui('Success! Picture files of graphs saved to nlp_keywords folder\n', '\n')
    # Turning both NLP sentiments csv files into a histogram graph with the sentiments per month
    print_console_gui('Processing NLP sentiment csv files into graphs', '\n')
    error_code = sgr.turn_sentiments_into_graph(search_term, start_date, end_date)
    if error_code == -1:
        print_console_gui('Failure :( Sentiment csv files not found', '\n\n')
    else:
        print_console_gui('Success! Picture file of graph saved to nlp_sentiments folder', '\n\n')

def process_graphs(entries):
    search_term = clean_search_text(entries[0][1].get())
    start_date = entries[1][1].get()
    end_date = entries[2][1].get()
    date_error_code = error_check_date(start_date, end_date)
    if date_error_code:
        graph_functions(search_term, start_date, end_date)

# makeform function code taken from https://www.python-course.eu/tkinter_entry_widgets.php
def makeform(root, fields):
    entries = []
    i = 0
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=30, text=field, anchor='w')
        ent = tk.Entry(row)
        ent.insert(10, text_list[i])
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
        i += 1
    return entries

# used some code from https://www.python-course.eu/tkinter_entry_widgets.php to build part of the GUI window
if __name__ == '__main__':
    root = tk.Tk()
    title = 'Tweet HealthPub Scraper NLP Analyzer'
    root.title(title)
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: start_processing(e)))   
    b1 = tk.Button(root, text='Submit', command=(lambda e=ents: start_processing(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Quit', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text='Process Graphs', command=(lambda e=ents: process_graphs(e)))
    b3.pack(side=tk.BOTTOM, padx=5, pady=5)
    text = tk.Text(height=30, width=56, bg='light gray')
    vsb = tk.Scrollbar(orient="vertical", command=text.yview)
    text.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    text.pack(side="left", fill="both", expand=True)
    print_console_gui('HealthPub/Tweet NLP Analysis Data/Chart Generator\n\n'
    'Note: Window may show \"Not Responding\" in the title bar, but it is actually '
    'working in the background.\n\nLook to command prompt window for more ongoing '
    'program information, if it is available.', '\n\n', '\n')
    root.mainloop()