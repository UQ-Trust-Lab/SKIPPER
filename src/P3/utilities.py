# -*- coding: utf-8 -*-

import spacy
nlp = spacy.load("en_core_web_sm")
# from spacy import en_core_web_sm
# nlp = en_core_web_sm.load()

def checkLocation(sentence):
    if check_noun(sentence) == False:
        return False
    doc = nlp(sentence)
    for sen in doc.sents:

        for token in sen:
            if token.text == "near":
                return True
            if token.text == 'Location' and token.pos_ == 'PROPN':
                return False
            if token.text =="to" or token.pos_ == "NOUN":
                for child in token.children:
                    if ("Locate" or "locate") in str(child):
                        return True
                    if "located" in str(child):
                        return False
        for chunk in sen.noun_chunks:
            if chunk.root.text == "states":
                return False
            if "MAC address" in chunk.text:
                return False

    return True

def checkEmail(sentence):
    if check_noun(sentence) == False:
        return False
    doc = nlp(sentence)
    for sen in doc.sents:
        for chunk in sen.noun_chunks:
            if chunk.text == "email address":
                return True
        for token in sen:
            if token.pos_=="NOUN" and token.head.text == "email":
                return False
    return True

def checkNumber(sentence):
    if check_noun(sentence) == False:
        return False
    doc = nlp(sentence)
    for sen in doc.sents:
        flag = 0
        for token in sen:
            if token.text == "our":
                flag += 1
            if token.text == "number":
                flag += 1
        if flag >= 2:
            return False
    return True

# check answer-based： if negative return false
def check_an_mood(sen):
    doc = nlp(sen)
    flag = 0
    for sen in doc.sents:
        for token in sen:
            if token.text == "not" or token.text == "no" or token.text == "n't" or token.text == "invalid" or token.text == "incorrect":
                return False
        flag += 1
        if flag >= 2:
            return True
    return True

#check confirmative response
def check_confirmative(sen):
    doc = nlp(sen)
    for sen in doc.sents:
        for token in sen:
            if token.text == "okay" or token.text == "ok" or token.text == "yes" or token.text == "sure" or token.text == "success" or token.text == "successful":
                return True
    return False

def check_noun(sentence):
    doc = nlp(sentence)
    for sen in doc.sents:
        for token in sen:
            if token.text.istitle() and token.pos_ == 'NOUN' and sentence.index(token.text) != 0:
                return False
    return True
