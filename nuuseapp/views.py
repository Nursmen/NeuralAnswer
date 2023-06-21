from django.shortcuts import render
from django.http import HttpResponse
import torch
from transformers import AutoTokenizer, AutoModel
from .models import QA
import torch.nn as nn
import numpy as np

import translators as ts

from .utils import *

tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")
modelemb = AutoModel.from_pretrained("cointegrated/rubert-tiny2")


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

questions.append('Какая сейчас погода?')
questions.append('Какой курс валюты сом к дургим валютам')
questions.append('Который час или сколько время.')
dig['WARNING'] = "Обратитесь к сотруднику таможни"

import numpy as np

sth = []

for i, j in enumerate(questions):
    sth.append(embed_bert_cls(j, modelemb, tokenizer))   
    
def index(request, text='Который час'):

    response = find(text, sth, questions)

    if response in dig.keys():
        response = dig[response]

    return HttpResponse(response)

def find(word, sth, context):
    scores = []
    for j,i in enumerate(sth):

        score = nn.functional.cosine_similarity(torch.from_numpy(i), torch.from_numpy(embed_bert_cls(word, modelemb, tokenizer)), 0)

        scores.append(score)

    idx = np.argmax(np.array(scores))

    if scores[idx] > 0.6:

        if context[idx] == 'Какая сейчас погода?':

            _ = [city:=i if i[0].isupper() else None for i in word.split(' ')[1:]]

            return weather(ts.translate_text(city, from_language='ru', to_language='en'), city)
        
        elif context[idx] == 'Какой курс валюты сом к дургим валютам':
            
            return rate()
        
        elif context[idx] == 'Который час или сколько время.':

            return current_time_ru()

        return context[idx]

    else:
        return 'WARNING'