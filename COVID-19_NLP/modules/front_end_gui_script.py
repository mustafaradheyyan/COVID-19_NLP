import sys
sys.path.insert(0, 'backend processing')
from health_pub_scraper import *
from tweet_to_dict import *
from process_nlp_output import *
import keywords_into_graph as kgr
import tkinter as tk

fields = 'Search Term', 'Start Date (mm-dd-yyyy)', 'End Date  (mm-dd-yyyy)',\
'Number of tweets per month', 'Number of health pubs per month'
text_list = 'COVID-19', "01-12-2020", '05-24-2021', 2, 1

def fetch(entries):
    # Getting user input from text entries in GUI window, defaults are set
    search_term = entries[0][1].get()
    start_date = entries[1][1].get()
    end_date = entries[2][1].get()
    pubs_per_month = float(entries[3][1].get())
    tweets_per_month = float(entries[4][1].get())

    # Reading health pub csv file and creating dictionary object
    print("\nScraping medRxiv " + search_term + " publication urls", flush = True)
    text.insert(tk.END, "Scraping medRxiv " + search_term + ' publication urls\n\n')
    dict_of_urls = health_pub_scraper(pubs_per_month, start_date, end_date, search_term)
    # Processing dictionary object with NLP to return a keywords and sentiments file
    # The 'health_pub' part of the string signifies the NLP file name and the ".url" is the NLP query type
    print("Success\n\nProcessing health pub urls with NLP", flush = True)
    text.insert(tk.END, "Success!\n\nProcessing health pub urls with NLP\n")
    get_nlp_keywords_and_sentiment_to_file(dict_of_urls, 'health_pub..url')
    
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
    get_nlp_keywords_and_sentiment_to_file(dict_of_text, 'tweet.text')

    # Turning (both) NLP keyword csv files into a histogram graph with the top keyword per month
    print("Success\n\nProcessing NLP keyword csv files into graphs", flush = True)
    text.insert(tk.END, "Success!\n\nProcessing NLP keyword csv files into graphs\n")
    kgr.turn_keywords_into_graph(search_term)
    print("Success! Picture files of graphs saved to nlp_keywords folder")
    text.insert(tk.END, "Success! Picture files of graphs saved to nlp_keywords folder\n\n")

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
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = tk.Button(root, text='Submit', command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Quit', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
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