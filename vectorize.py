import datetime
import pandas as pd
from gensim import models, corpora, similarities

lda = models.ldamodel.LdaModel.load("data/lda/lda.model")
d = corpora.Dictionary.load_from_text("data/lda/dict.txt")

def vectorize(df):
    df['vector'] = df['tokens'].apply(
        lambda x: lda.get_document_topics(d.doc2bow(x.split()), minimum_probability=0.0)
    ).apply(lambda x: [tp[1] for tp in x])
    return df[['article_id', 'vector']]

if __name__ == "__main__":    
    from database import get_article_tokens, insert_vector_data
    since = datetime.date.today() - datetime.timedelta(days=2)
    df = get_article_tokens(since)
    df = vectorize(df)

    insert_vector_data(df)
