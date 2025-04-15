from rank_bm25 import BM25Okapi
from db.base_db import BaseDB
from config import db_hyperparameter


class VectorDB(BaseDB):
    def __init__(self):
        self.texts = []
        self.tokenized_corpus = []
        self.bm25 = None
        self.k = db_hyperparameter["k"]
        self.bm25th = db_hyperparameter["bm25threshold"]

    def put(self, txt):
        self.texts.append(txt)
        tokenized = self._tokenize(txt)
        self.tokenized_corpus.append(tokenized)
        self._update_bm25()

    def get(self, query_txt):
        if not self.texts or self.k <= 0:
            return []

        query_tokens = self._tokenize(query_txt)
        scores = self.bm25.get_scores(query_tokens)
        scored_docs = list(zip(scores, self.texts))

        # Filter out documents with score lower than th
        scored_docs = [doc for doc in scored_docs if doc[0] >= self.bm25th]
        # Sort by descending score, then ascending text for determinism
        scored_docs.sort(key=lambda x: (-x[0], x[1]))

        return scored_docs[:self.k]

    def _tokenize(self, text):
        return text.lower().split()

    def _update_bm25(self):
        self.bm25 = BM25Okapi(self.tokenized_corpus)
