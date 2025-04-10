from db.base_db import BaseDB
from typing import Dict, List


class KeywordDB(BaseDB):
    def __init__(self):
        self.store = {}

    def get(self, info: List[str]) -> str:
        """
        info: in KeywordDB is a list of keywords
        """
        retrieved_info = ""
        for keyword in info:
            retrieved_info += self.store[keyword]
        return retrieved_info

    def set(self, info):
        """
        :param info: formated as dict[keywords, string of information]
        """
        for keyword in info:
            if keyword not in self.store:
                self.store[keyword] = ""
            self.store[keyword] += " " + info[keyword]
