import process_nlp_output as pnlp
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions, SentimentOptions

#Authentication via IAM
def nlu_authenticator(api_key, service_url):
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(service_url)
    return natural_language_understanding

def generate_nlp_output(nlp_input, type_of_query, user_api_key, user_service_url):
    if type_of_query[1:] == 'url':
        return generate_nlp_output_from_url_dict(nlp_input, user_api_key, user_service_url)
    elif type_of_query == 'text':
        return generate_nlp_output_from_text_dict(nlp_input, user_api_key, user_service_url)

def generate_nlp_output_from_text_dict(text_dict, api_key, service_url):
    nlu = nlu_authenticator(api_key, service_url)
    #file_list = []
    nlp_dict = {}
    for date, text in text_dict.items():
        nlp_list = []
        for tweet in text:
            nlp_list.append(nlu.analyze(text=tweet,features=Features(keywords=KeywordsOptions\
            (sentiment=True,emotion=True,limit=2),sentiment=SentimentOptions()),language='en').get_result())
        file_name = str('nlp_results_' + date.replace('/', '-') + '.csv')
        #file_list.append(file_name)
        nlp_dict[date] = nlp_list
        write_results_to_keyword_file('nlp_tweet_keywords.csv', nlp_list)
        write_results_to_sentiment_file('nlp_tweet_sentiments.csv', nlp_dict)
    return file_name

def generate_nlp_output_from_url_dict(url_dictionary, api_key, service_url):
    nlu = nlu_authenticator(api_key, service_url)
   # file_list = []
    nlp_dict = {}
    for date, row in url_dictionary.items():
        nlp_list = []
        for url in row:
            nlp_list.append(nlu.analyze(url=url,features=Features(keywords=KeywordsOptions\
            (sentiment=True,emotion=True,limit=2),sentiment=SentimentOptions())).get_result())
        file_name = str('nlp_results_' + date.replace('/', '-') + '.csv')
       # file_list.append(file_name)
        nlp_dict[date] = nlp_list
    write_results_to_keyword_file('health_pub_nlp_keywords.csv', nlp_dict)
    write_results_to_sentiment_file('health_pub_nlp_sentiments.csv', nlp_dict)
    return file_name

def write_results_to_keyword_file(file_name, keyword_dict):
    date_keyword_dict = {}
    with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        for date, nlp_list in keyword_dict.items():
            #print('keyword nlp_list:')
            #print(nlp_list)
            keyword_list = []
            for keyword in nlp_list[0]['keywords']:
                    #print(keyword['text'])
                   # print('text in keyword[0][\'text\']')
                    #print(text)
                    keyword_list.append(keyword['text'])#['text'])
            date_keyword_dict[date] = keyword_list
        #print(pub_nlp_list[0]['keywords'][0]['text'])
        pnlp.write_to_file(date_keyword_dict, file_name, ['Date', 'Keywords'])

def write_results_to_sentiment_file(file_name, sentiment_dict):
    date_sentiment_dict = {}
    with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        for date, nlp_list in sentiment_dict.items():
            print('sentiment nlp_list:')
            print(nlp_list)
            sentiment_list = []
            for sentiment in nlp_list:
                print('sentiment in nlp_list:')
                print(sentiment)
                print('score in sentiment in nlp_list:')
                print(sentiment['sentiment']['document']['score'])
                #for label in sentiment['sentiment']['document']:
                #    for score in label:
                 #       print('label[0] in sentiment score:')
                 #       print(score)
                    #print(sentiment['score'])
                sentiment_list.append(sentiment['sentiment']['document']['score'])#['score'])
            date_sentiment_dict[date] = sentiment_list
        #print(pub_nlp_list[0]['sentiment'][0]['text'])
        pnlp.write_to_file(date_sentiment_dict, file_name, ['Date', 'Sentiment'])