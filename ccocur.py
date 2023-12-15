from sklearn.feature_extraction.text import CountVectorizer

from vetor import postprocessor


class MyTokenizer:
    def __init__(self, tagger):
        self.tagger = tagger
    def __call__(self, sent):
        pos = self.tagger.pos(sent)
        pos = ['{}/{}'.format(word,tag) for word, tag in pos]
        return pos


filename = 'C:/Users/lixxc/Desktop/자연언어처리 기말/종로구grapg(2023)'

with open('C:/Users/lixxc/Desktop/자연언어처리 기말/단어' + filename + '.txt', 'r') as ft:
    text = ft.readlines()


my_tokenizer = MyTokenizer(postprocessor)
vectorizer = CountVectorizer(tokenizer = my_tokenizer)
X = vectorizer.fit_transform(text)

Xc = (X.T * X)
Xc.setdiag(0)
print(Xc.todense())

# pandas 를 사용하여 gephi 에서 보여줄 word-word co-occurrence matrix csv 파일을 생성
names = vectorizer.get_feature_names() # 엔티티 이름들을 보여준다
df = pd.DataFrame(data = Xc.toarray(), columns = names, index = names)
df.to_csv('C:/Users/lixxc/Desktop/자연언어처리 기말/' + filename + '.csv', sep = ',')