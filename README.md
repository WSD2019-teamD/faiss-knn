# faiss-knn

`GET /knn?id=<article_id>&count=<k>` でk個の近傍の記事idを取得

`id`: Qiitaの記事id
`count`: 近傍探索の個数

### setup
`unzip data/vec.csv.zip -d data`
`docker-compose up -d`
### query test
`curl 'localhost:9000/knn?id=<article_id>&count=<k>' | jq .`
