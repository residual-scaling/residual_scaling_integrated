from rank_bm25 import BM25Okapi
from db.base_db import BaseDB


class BM25Database(BaseDB):
    def __init__(self):
        self.texts = []
        self.tokenized_corpus = []
        self.bm25 = None

    def put(self, txt):
        """
        Add a text document to the database
        """
        self.texts.append(txt)
        tokenized = self._tokenize(txt)
        self.tokenized_corpus.append(tokenized)
        self._update_bm25()

    def get(self, query_txt, k):
        """
        Retrieve top k documents with highest BM25 scores for the query
        Returns list of tuples (score, text) sorted by descending score
        """
        if not self.texts or k <= 0:
            return []

        query_tokens = self._tokenize(query_txt)
        scores = self.bm25.get_scores(query_tokens)
        scored_docs = list(zip(scores, self.texts))

        # Sort by descending score, then ascending text for determinism
        scored_docs.sort(key=lambda x: (-x[0], x[1]))

        return scored_docs[:k]

    def _tokenize(self, text):
        """
        Basic tokenizer that splits on whitespace and lowercases
        """
        return text.lower().split()

    def _update_bm25(self):
        """
        Rebuild BM25 index with current corpus
        """
        self.bm25 = BM25Okapi(self.tokenized_corpus)