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
    nlu = nlu_authenticator(user_api_key, user_service_url)
    if type_of_query[1:] == 'url':
        return generate_nlp_output_from_url_dict(nlp_input, nlu)
    elif type_of_query == 'text':
        return generate_nlp_output_from_text_dict(nlp_input, nlu)

def generate_nlp_output_from_text_dict(text_dict, nlu):
    nlp_dict = {}
    for date, text in text_dict.items():
        nlp_list = []
        for tweet in text:
            nlp_list.append(nlu.analyze(text=tweet,features=Features(keywords=KeywordsOptions\
            (sentiment=True,emotion=True,limit=2),sentiment=SentimentOptions()),language='en').get_result())
        nlp_dict[date] = nlp_list
    return nlp_dict

def generate_nlp_output_from_url_dict(url_dictionary, nlu):
    nlp_dict = {}
    for date, row in url_dictionary.items():
        nlp_list = []
        for url in row:
            nlp_list.append(nlu.analyze(url=url,features=Features(keywords=KeywordsOptions\
            (sentiment=True,emotion=True,limit=2),sentiment=SentimentOptions())).get_result())
        nlp_dict[date] = nlp_list
    return nlp_dict