import datetime
import pandas as pd
from gensim import models, corpora, similarities

lda = models.ldamodel.LdaModel.load("data/lda/lda.model")
d = corpora.Dictionary.load_from_text("data/lda/dict.txt")
vec_path = './data/vec2.csv'

def vectorize(df):
    df['vector'] = df['tokens'].apply(
        lambda x: lda.get_document_topics(d.doc2bow(x.split()), minimum_probability=0.0)
    ).apply(lambda x: [tp[1] for tp in x])
    return df[['article_id', 'vector']]

