import sys
sys.path.insert(0, 'backend processing')
from health_pub_scraper import *
from tweet_to_dict import *
from generate_nlp_output import *
from process_nlp_output import *
import sentiments_into_graph as sgr
import keywords_into_graphs as kgr
import tkinter as tk

fields = 'Search Term', 'Start Date (mm-dd-yyyy)', 'End Date  (mm-dd-yyyy)',\
'Number of tweets per month', 'Number of health pubs per month', 'IBM Watson NLU API Key',\
'IBM Watson Service URL'
text_list = 'COVID-19', "05-12-2020", '08-24-2020', 1, 1, '4Ac-fI2WAly37w3y9EFyLbadnail9QU-hUk9shNck1eE',\
'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/347c5943-5b2f-435f-a501-4807978a45f6'

def fetch(entries):
    # Getting user input from text entries in GUI window, defaults are set
    search_term = entries[0][1].get()
    start_date = entries[1][1].get()
    end_date = entries[2][1].get()
    pubs_per_month = float(entries[3][1].get())
    tweets_per_month = float(entries[4][1].get())
    user_api_key = entries[5][1].get()
    user_service_url = entries[6][1].get()
    return search_term, start_date, end_date, pubs_per_month, tweets_per_month, user_api_key, user_service_url

def start_processing(entries):
    search_term, start_date, end_date, pubs_per_month, tweets_per_month, user_api_key, user_service_url = fetch(entries)

    # Reading health pub csv file and creating dictionary object
    print("\nScraping medRxiv " + search_term + " publication urls", flush = True)
    text.insert(tk.END, "Scraping medRxiv " + search_term + ' publication urls\n')
    dict_of_urls = health_pub_scraper(pubs_per_month, start_date, end_date, search_term)
    # Processing dictionary object with NLP to return a keywords and sentiments file
    # The 'health_pub' part of the string signifies the NLP file name and the ".url" is the NLP query type
    print("Success\n\nProcessing health pub urls with NLP", flush = True)
    text.insert(tk.END, "Success!\n\nProcessing health pub urls with NLP\n")
    get_nlp_keywords_and_sentiment_to_file(dict_of_urls, 'health_pub..url', user_api_key, user_service_url)
    
    # Getting English tweets from Twitter based on dates and search term
    print("Success\n\nScraping Twitter tweets", flush = True)
    text.insert(tk.END, "Success!\n\nScraping Twitter tweets\n")
    tweet_scraper(tweets_per_month, start_date, end_date, search_term)
    # Reading tweets csv files and creating a dictionary object from it
    print("Success\n\nConverting tweet csv files into a text dictionary", flush = True)
    text.insert(tk.END, "Success!\n\nConverting tweet csv files into a text dictionary\n")
    dict_of_text = get_tweet_csv_data_into_text_dict(start_date, end_date, search_term)
    # Processing dictionary object with NLP to return a keywords and sentiments file
    # The 'tweet' part of the string signifies the NLP file name and the "text" is the NLP query type
    print("Success\n\nProcessing tweets with NLP", flush = True)
    text.insert(tk.END, "Success!\n\nProcessing tweets with NLP\n")
    get_nlp_keywords_and_sentiment_to_file(dict_of_text, 'tweet.text', user_api_key, user_service_url)

    # Turning (both) NLP keyword csv files into histogram graphs with the top keyword per month
    text.insert(tk.END, "Success!\n\nProcessing NLP keyword csv files into graphs\n")
    kgr.turn_keywords_into_graphs(search_term)
    print("Success! Picture files of graphs saved to nlp_keywords folder\n")
    text.insert(tk.END, "Success! Picture files of graphs saved to nlp_keywords folder\n\n")

    # Turning both NLP sentiments csv files into a histogram graph with the sentiments per month
    print("Processing NLP sentiment csv files into graphs", flush = True)
    text.insert(tk.END, "Processing NLP sentiment csv files into a graph\n")
    sgr.turn_sentiments_into_graph(search_term)
    print("Success! Picture file of graph saved to nlp_sentiments folder", flush = True)
    text.insert(tk.END, "Success! Picture file of graph saved to nlp_sentiments folder\n\n")

def process_graphs(entries):
    search_term = entries[0][1].get()

    # Turning (both) NLP keyword csv files into histogram graphs with the top keyword per month
    print("\nProcessing NLP keyword csv files into graphs", flush = True)
    text.insert(tk.END, "Processing NLP keyword csv files into graphs\n")
    kgr.turn_keywords_into_graphs(search_term)
    print("Success! Picture files of graphs saved to nlp_keywords folder\n")
    text.insert(tk.END, "Success! Picture files of graphs saved to nlp_keywords folder\n\n")

    # Turning both NLP sentiments csv files into a histogram graph with the sentiments per month
    print("Processing NLP sentiment csv files into graphs", flush = True)
    text.insert(tk.END, "Processing NLP sentiment csv files into a graph\n")
    sgr.turn_sentiments_into_graph(search_term)
    print("Success! Picture file of graph saved to nlp_sentiments folder", flush = True)
    text.insert(tk.END, "Success! Picture file of graph saved to nlp_sentiments folder\n\n")

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
    text.insert(tk.END, 'HealthPub/Tweet NLP Analysis Data/Chart Generator\n\n'
    'Note: Window may show \"Not Responding\" in the title bar, but it is actually '
    'working in the background.\n\nLook to command prompt window for more ongoing '
    'program information, if it is available.\n\n')
    print('\nHealthPub/Tweet NLP Analysis Data/Chart Generator\n\n'
    'Note: GUI window may show \"Not Responding\" in the title bar, but it is actually '
    'working in the background.\n\nLook here for more ongoing program information!', flush = True)
    root.mainloop()