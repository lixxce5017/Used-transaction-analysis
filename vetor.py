from konlpy.tag import Okt
from konlpy.utils import pprint
from collections import Counter
from ckonlpy.tag import Postprocessor
from ckonlpy.tag import Twitter
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from gensim import corpora, models
import pyLDAvis
import pyLDAvis.gensim as gensimvis
import codecs

from ckonlpy.utils import load_wordset
passwords = load_wordset('passwords.txt')
stopwords = load_wordset('stopwords.txt')

from ckonlpy.utils import load_replace_wordpair
replace = load_replace_wordpair('replace.txt')

from ckonlpy.utils import load_ngram
ngrams = load_ngram('ngrams.txt')

Okt = Okt()
twitter = Twitter()


new_nouns = []

with open('C:/Users/lixxc/Desktop/자연언어처리 기말/추가딕셔너리.txt', encoding='utf8') as fd:
    for line in fd:
        new_nouns.append(line.strip('\n'))

twitter.add_dictionary(new_nouns, 'Noun')

passtags = {'Noun'}

postprocessor = Postprocessor(
    base_tagger = twitter,
    stopwords = stopwords,
    #passwords = passwords,
    passtags = passtags,
    replace = replace,
    ngrams = ngrams
)

token = []
nouns = []

class MyTokenizer:
    def __init__(self, tagger):
        self.tagger = tagger
    def __call__(self, sent):
        pos = self.tagger.pos(sent)
        pos = ['{}/{}'.format(word,tag) for word, tag in pos]
        return pos


filename = '서울/종로구(2023)'

with open('C:/Users/lixxc/Desktop/자연언어처리 기말/단어/' + filename + '.txt', 'r') as ft:
    text = ft.readlines()


my_tokenizer = MyTokenizer(postprocessor)
vectorizer = CountVectorizer(tokenizer = my_tokenizer)
X = vectorizer.fit_transform(text)

Xc = (X.T * X) # this is co-occurrence matrix in sparse csr format
Xc.setdiag(0) # sometimes you want to fill same word cooccurence to 0
print(Xc.todense()) # print out matrix in dense format



names = vectorizer.get_feature_names() # 엔티티 이름들을 보여준다
df = pd.DataFrame(data = Xc.toarray(), columns = names, index = names)
df.to_csv('C:/Users/lixxc/Desktop/자연언어처리 기말/csv파일/' + filename + '.csv', sep = ',')

for s in text:
    pre_nouns = postprocessor.pos(s)
    for w in pre_nouns:
        nouns.append(w[0])
    if(len(nouns)!=0):
        token.append(nouns)
    nouns = []

f = codecs.open('C:/Users/lixxc/Desktop/자연언어처리 기말/단어/' + filename+"_preprocessed.txt", 'w', encoding='utf-8')
f.write(str(token))

id2word = corpora.Dictionary(token)
totalCorpus = token



## 출현단어 2개 이하는 무시하고 dictionary 생성

min_count = 3
word_counter = Counter((word for words in token for word in words))
removal_word_idxs = {
    id2word.token2id[word] for word, count in word_counter.items()
    if count < min_count
}

id2word.filter_tokens(removal_word_idxs)
id2word.compactify()
print('dictionary size : %d' % len(id2word))

## Term - Document Matrix 생성
corpus = [id2word.doc2bow(text) for text in totalCorpus]


"""
lda_model = models.ldamodel.LdaModel(corpus=corpus,
id2word=id2word,
num_topics=20,
random_state=100,
update_every=1,
chunksize=100,
passes=10,
alpha='auto',
per_word_topics=True)
"""

# mallet lda 적용
mallet_path = 'source/mallet-2.0.8/bin/mallet'
lda_model = models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=id2word)

pprint(lda_model.print_topics())

# Compute Coherence Score
coherence_model_lda = models.CoherenceModel(model=lda_model, texts=totalCorpus, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)


lda_model = models.wrappers.ldamallet.malletmodel2ldamodel(lda_model)


prepared_data = gensimvis.prepare(lda_model, corpus, id2word)
pyldavis_html_path = 'C:/Users/lixxc/Desktop/자연언어처리 기말/html모음/' + filename + '.html'
pyLDAvis.save_html(prepared_data, pyldavis_html_path)