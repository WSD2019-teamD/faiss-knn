FROM continuumio/anaconda3

RUN /opt/conda/bin/conda install faiss-cpu -c pytorch -y

WORKDIR /root/faiss-knn

ENTRYPOINT /opt/conda/bin/python3 main.py 0.0.0.0 9000
