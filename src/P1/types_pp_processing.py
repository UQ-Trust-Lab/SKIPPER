import csv
import re
import spacy
from bs4 import BeautifulSoup

from nltk.corpus import stopwords, wordnet
from text_preprocessing import pre_process,pre_process_type
from sentence_bayesian import clf_type,tf
from phrase_similarity import wordnetSim3




replacement_patterns = [
(r'won\'t', 'will not'),
(r'can\'t', 'cannot'),
(r'i\'m', 'i am'),
(r'ain\'t', 'is not'),
(r'(\w+)\'ll', '\g<1> will'),
(r'(\w+)n\'t', '\g<1> not'),
(r'(\w+)\'ve', '\g<1> have'),
(r'(\w+)\'s', '\g<1> is'),
(r'(\w+)\'re', '\g<1> are'),
(r'(\w+)\'d', '\g<1> would')]

class RegexpReplacer(object):
    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
        return s
# 获取单词的词性
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def cleanHtml(txt):
    stop_words = set(stopwords.words('english'))
    stop_words.add("")
    personal_information = []

    with open(txt, encoding='utf-8') as file_obj:
        for line in file_obj:
            personal_information.append(line)

    text = ''.join(personal_information)
    soup = BeautifulSoup(text,'html.parser')
    lower = soup.get_text().lower()
    replacer = RegexpReplacer()
    lower = replacer.replace(lower)
    lower = re.sub(r'\s+', ' ', lower)
    lower = re.sub(r':',".",lower)
    lower = re.sub(r"e.g.","",lower)
    lower = re.sub(r"-", "", lower)
    lower = pre_process(lower)
    sentence_list = lower.split(".")
    return sentence_list

def writeSentenceFirst(sentence_list):
    f = open('personal_type.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(f,dialect='unix')
    csv_writer.writerow(["mark", "sentence"])
    for sentence in sentence_list:
        csv_writer.writerow(['0', sentence])
    f.close()

def writeSentence(sentence_list):
    f = open('personal_type.csv', 'a', encoding='utf-8')
    csv_writer = csv.writer(f, dialect='unix')
    for sen in sentence_list:
        csv_writer.writerow(['0', sen])
    f.close()

def caculateSim(txt):
    information_type = ["name", "email address", "phone number", "billing","birth date", "age",'user id', "gender", "location","job title",
                        "phonebook", "sms", "income","ip","internet protocol","marital","social security number",'credit card',
                        "type browser","browser version","operate system","postal address","postcode","profile","education","occupation","student","software",
                        "driver","insurance","health","signature","province","time zone","isp","tax","device id","domain name",
                        "prior usage","cookie","web page","interact site","device information","dash cam",
                        "log data","page service visit","time spend page","time date visit","time date use service","demographic information","country","usage pattern","language","reminder","alexa notification","amazon pay"]
    sentence_list = cleanHtml(txt)
    for sen in sentence_list:
        sentence_list[sentence_list.index(sen)] = pre_process_type(sen)

    word = []
    simList = []
    for a in information_type:
        word.append(0)
    for b in information_type:
        simList.append(0)
    for sentence in sentence_list:
        for type in information_type:
            if type in sentence:
                if type == "age" or type == "interest":
                    if sentence.index(type) - 1 == " ":
                        word[information_type.index(type)] = 1
                else:
                    word[information_type.index(type)] = 1
        if clf_type.predict(tf.transform([sentence])) == "1":
            nlp = spacy.load('en_core_web_sm')
            doc = nlp(sentence)
            chunk_list = []
            for chunk in doc.noun_chunks:
                chunk_str = str(chunk)
                if chunk_str[0] == " ":
                    chunk_str = chunk_str[1:]
                chunk_list.append(chunk_str)
            for type in information_type:
                for chunk in chunk_list:
                    if type == chunk:
                        word[information_type.index(type)] = 1
                        chunk_list.remove(chunk)
            for type in information_type:
                for chunk in chunk_list:
                    try:
                        if wordnetSim3(chunk,type) > 0.8:
                            simList[information_type.index(type)] = wordnetSim3(chunk,type)
                    except Exception:
                        pass
                        print("error")
            nowMax = 0
            for max in simList:
                if max > nowMax:
                    nowMax = max
            if nowMax != 0:
                word[simList.index(nowMax)] = 1
    return word








