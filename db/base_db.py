from typing import Dict, List


class BaseDB:
    def get(self, info: List[str]) -> str:
        pass

    def set(self, info):
        pass
