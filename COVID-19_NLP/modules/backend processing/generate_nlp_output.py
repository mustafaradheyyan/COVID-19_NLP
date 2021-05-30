import csv
from tkinter import messagebox
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions, SentimentOptions

#Authentication via IAM
authenticator = IAMAuthenticator('4Ac-fI2WAly37w3y9EFyLbadnail9QU-hUk9shNck1eE')
natural_language_understanding = NaturalLanguageUnderstandingV1(
              version='2020-08-01', authenticator=authenticator)

natural_language_understanding.set_service_url('https://api.'
        'us-south.natural-language-understanding.watson.cloud.ibm.com'
        '/instances/347c5943-5b2f-435f-a501-4807978a45f6')

def generate_nlp_output(nlp_input, type_of_query):
    if type_of_query[1:] == 'url':
        return generate_nlp_output_from_url_dict(nlp_input)
    elif type_of_query == 'text':
        return generate_nlp_output_from_text_dict(nlp_input)

def generate_nlp_output_from_text_dict(text_dict):
    file_list = []
    for date, text in text_dict.items():
        nlp_list = []
        for tweet in text:
            try:
                nlp_list.append(natural_language_understanding.analyze(text=tweet,
                        features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2),\
                        sentiment=SentimentOptions()),language='en').get_result())
            except:
               messagebox.showinfo("IBM Watson API Error", "An error occurred with Watson API NLP parsing tweet")
        file_name = str('nlp_results_' + date.replace('/', '-') + '.csv')
        file_list.append(file_name)
        write_text_results_to_file(file_name, nlp_list)
    return file_list

def generate_nlp_output_from_url_dict(url_dictionary):
    file_list = []
    for date, row in url_dictionary.items():
        nlp_list = []
        for url in row:
            try:
                nlp_list.append(natural_language_understanding.analyze(url=url,
                        features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2),\
                        sentiment=SentimentOptions())).get_result())
            except:
                messagebox.showinfo("IBM Watson API Error", 'An error occurred with Watson API NLP parsing\n' + str(url))
        file_name = str('nlp_results_' + date.replace('/', '-') + '.csv')
        file_list.append(file_name)
        write_url_results_to_file(file_name, nlp_list)
    return file_list

def write_text_results_to_file(file_name, pub_nlp_list):
    with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['a','b','c','Sentiment','d','e','Keyword1','f','g',\
                        'h','i','j','k','l','m','n','Keyword2','o']
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        for item in pub_nlp_list:
            csv_file.write("%s\n" % item)

def write_url_results_to_file(file_name, pub_nlp_list):
    with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['a','b','c','Sentiment','d','e','f','Keyword1','g',\
                        'h','i','j','k','l','m','n','o','Keyword2']
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        for item in pub_nlp_list:
            csv_file.write("%s\n" % item)
