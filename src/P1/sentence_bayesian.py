import csv


from sklearn.metrics import f1_score, recall_score
from sklearn.naive_bayes import MultinomialNB

from text_preprocessing import pre_process_title
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def readtrain():
    with open('../../dataset/training_data/personal_type.csv', 'rt') as csvfile:
        reader = csv.reader(csvfile)
        column1 = [row for row in reader]
    content_train = [i[0] for i in column1[1:]]
    opinion_train = [i[1] for i in column1[1:]]

    train = [content_train, opinion_train]
    return train

def segmentWord(cont):
    c = []
    for i in cont:
        clean_text = pre_process_title(i)
        c.append(clean_text)
    return c
train = readtrain()
content = segmentWord(train[1])

textMark = train[0]

train_content = content[:499]
# test_content = content[400:450]
train_textMark = textMark[:499]
# test_textMark = textMark[400:450]

tf = TfidfVectorizer(max_df=0.5)

train_features = tf.fit_transform(train_content)


clf_type = MultinomialNB(alpha=0.1)
clf_type.fit(train_features,train_textMark)



