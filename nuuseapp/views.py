from django.shortcuts import render
from django.http import HttpResponse
import torch
from transformers import AutoTokenizer, AutoModel
from .models import QA, QA_en
import torch.nn as nn
import numpy as np

import translators as ts

from .utils import *

tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")
modelemb = AutoModel.from_pretrained("cointegrated/rubert-tiny2")

tokenizer_en = AutoTokenizer.from_pretrained("prajjwal1/bert-tiny")
modelemb_en = AutoModel.from_pretrained("prajjwal1/bert-tiny")




def embed_bert_cls(text, model, tokenizer):
    t = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()



    
objects = QA.objects.all()

dig = {}
questions = []
for i in objects:
    dig[i.question] = i.answer
    questions.append(i.question)

dig['WARNING'] = "Обратитесь к сотруднику таможни"


sth = []

for i, j in enumerate(questions):
    sth.append(embed_bert_cls(j, modelemb, tokenizer))   




objects = QA_en.objects.all()

dig_en = {}
questions_en = []
for i in objects:
    dig_en[i.question] = i.answer
    questions_en.append(i.question)

dig_en['WARNING'] = "Contact a customs officer"

sth_en = []

for i, j in enumerate(questions_en):
    sth_en.append(embed_bert_cls(j, modelemb_en, tokenizer_en))   
    




def index(request, text='What is the rate of som against dollar', lang='en'):


    something = sth if lang == 'ru' else sth_en
    context = questions if lang == 'ru' else questions_en

    response = find(text, something, context, lang)

    dictinary = dig if lang == 'ru' else dig_en

    if response in dictinary.keys():
        response = dictinary[response]

    return HttpResponse(response)





def find(word, sth, context, lang):
    scores = []

    model = modelemb if lang == 'ru' else modelemb_en
    token = tokenizer if lang == 'ru' else tokenizer_en

    for j,i in enumerate(sth):

        score = nn.functional.cosine_similarity(torch.from_numpy(i), torch.from_numpy(embed_bert_cls(word, model, token)), 0)

        scores.append(score)

    idx = np.argmax(np.array(scores))

    if scores[idx] > 0.85:

        if context[idx] == 'Какая сейчас погода?':

            _ = [city:=i if i[0].isupper() else None for i in word.split(' ')[1:]]

            if city == None:
                city = 'Бишкек'

            return weather(ts.translate_text(city, from_language='ru', to_language='en', translator='google'), city)
        
        elif context[idx] == 'What\'s the weather like now?':

            _ = [city:=i if i[0].isupper() else None for i in word.split(' ')[1:]]

            if city == None:
                city = 'Bishkek'

            return weather_en(city)
        
        elif context[idx] == 'Какой курс валюты сом к другим валютам.':
            
            return rate()
        
        elif context[idx] == 'What is the exchange rate of Kyrgyz som against other currencies.':
            
            return rate_en()
        
        elif context[idx] in ['Сколько время?', 'Который час?']:

            return current_time_ru()
        
        elif context[idx] == 'What time is it?':

            return current_time_en()

        return context[idx]

    else:
        return 'WARNING'