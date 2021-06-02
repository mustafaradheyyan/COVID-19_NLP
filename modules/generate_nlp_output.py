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

def generate_nlp_output(nlp_input, type_of_query, user_api_key, user_service_url, number_of_keywords):
    nlu = nlu_authenticator(user_api_key, user_service_url)
    if type_of_query == 'url':
        return generate_nlp_output_from_url_dict(nlp_input, nlu, number_of_keywords)
    elif type_of_query == 'text':
        return generate_nlp_output_from_text_dict(nlp_input, nlu, number_of_keywords)

def analyze_text_nlp(nlu, tweet, number_of_keywords):
    try:
        return nlu.analyze(text=tweet,features=Features(keywords=KeywordsOptions\
           (sentiment=True,emotion=True,limit=number_of_keywords),sentiment=SentimentOptions()),\
           language='en').get_result()
    except:
        return -1

def analyze_url_nlp(nlu, url, number_of_keywords):
    try:
        return nlu.analyze(url=url,features=Features(keywords=KeywordsOptions\
            (sentiment=True,emotion=True,limit=number_of_keywords),sentiment=SentimentOptions())).get_result()
    except:
        return -1

def generate_nlp_output_from_text_dict(text_dict, nlu, number_of_keywords):
    nlp_dict = {}
    for date, text in text_dict.items():
        nlp_list = []
        for tweet in text:
            nlp_list.append(analyze_text_nlp(nlu, tweet, number_of_keywords))
        nlp_dict[date] = nlp_list
    return nlp_dict

def generate_nlp_output_from_url_dict(url_dictionary, nlu, number_of_keywords):
    nlp_dict = {}
    for date, row in url_dictionary.items():
        nlp_list = []
        for url in row:
            nlp_list.append(analyze_url_nlp(nlu, url, number_of_keywords))
        nlp_dict[date] = nlp_list
    return nlp_dict