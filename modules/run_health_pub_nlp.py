import sys
import os
sys.path.insert(0, 'backend processing')
from process_nlp_output import *

def main():
    pub_csv = open_read_csv_file('CSVs/health_publication_information.csv')
    pub_url_dictionary = create_dictionary_object(pub_csv)
    get_nlp_keywords_and_sentiment_to_file(pub_url_dictionary, 'health_pub..url')

if __name__ == '__main__':
  main()
