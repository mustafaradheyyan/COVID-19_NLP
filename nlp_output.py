import numpy as np
import nlp as nlp
from read_csv import *

def is_number(price_value):
    try:
        price = float(price_value)
        return price
    except ValueError:
        return 0

def write_header(csv_file, fieldnames):
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()

def separate_list_with_date(date, data):
    concat_word = (date + ',')
    for word in data:
        concat_word = (concat_word + word + ',')
    return concat_word.split(',')

def write_to_file(dictionary, file_name, fieldnames):
    with open(file_name, mode='w', newline='') as csv_file:
        write_header(csv_file, fieldnames)
        writer = csv.writer(csv_file)
        for date, data in dictionary.items():
            if type(data) == list:
                word_list = separate_list_with_date(date, data)
                writer.writerow(word_list)
            else:
                writer.writerow([date,data])

def calculate_sentiment(nlp_data):
    sentiment_score = 0.0
    sentiment_count = 0
    for pub_data in nlp_data:
        for row in pub_data:
            positions=[x for x in range(len(row.split()))if row.split()[x]=='{\'score\':']
            if positions:
                for position in positions:
                    sentiment_score += is_number(row.split()[position + 1])
                    sentiment_count += 1
    return sentiment_score / sentiment_count

def calculate_keywords(nlp_data):
    keywords = []
    for pub_data in nlp_data:
        for row in pub_data:
            position = row.find('{\'text\':')
            if position >= 0:
                keywords.append(row[position+10:][:-1])
    return keywords

def sort_nlp_output(nlp_file_names, type_of_query):
    sentiment_dictionary = {}
    keyword_dictionary = {}
    for file in nlp_file_names:
        date = file[-14:-4]
        if type_of_query == 'url':
            nlp_data = np.loadtxt(file,dtype=str,delimiter=',',skiprows=1,usecols=(3,7,17))
        elif type_of_query == 'text':
            nlp_data = np.loadtxt(file,dtype=str,delimiter=',',skiprows=1,usecols=(3,6))
        os.remove(file)
        sentiment_dictionary[date] = calculate_sentiment(nlp_data)
        keyword_dictionary[date] = calculate_keywords(nlp_data)
    return keyword_dictionary, sentiment_dictionary

def get_nlp_keywords_and_sentiment_to_file(nlp_dictionary, type_of_query):
    nlp_file_names = nlp.generate_nlp_output(nlp_dictionary, type_of_query)
    keyword_dic, sentiment_dic = sort_nlp_output(nlp_file_names, type_of_query)
    write_to_file(keyword_dic, 'nlp_keywords.csv', ['Date', 'Keywords'])
    write_to_file(sentiment_dic, 'nlp_sentiments.csv', ['Date', 'Sentiment'])

def main():
    pub_csv_header, pub_csv = open_read_csv_file('CSVs/health_publication_information_test.csv')
    pub_url_dictionary = create_dictionary_object(pub_csv)
    get_nlp_keywords_and_sentiment_to_file(pub_url_dictionary, 'url')

if __name__ == '__main__':
  main()
