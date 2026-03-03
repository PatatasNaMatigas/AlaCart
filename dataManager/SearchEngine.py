from nltk.stem import SnowballStemmer
from collections import defaultdict

from dataManager.DataModels import Items

class SearchEngine:

    def __init__(self, item_manager: Items):
        self.raw_items = item_manager.getItems()
        self.stemmer = SnowballStemmer("english")
        self.index = defaultdict(list)
        self._build_index()

    def _build_index(self) -> None:
        for idx, item in enumerate(self.raw_items):
            text = f"{item['name']} {' '.join(item['tags'])}"
            words = set(self.stemmer.stem(w.lower()) for w in text.split())
            for word in words:
                self.index[word].append(idx)

    def search(self, query: str) -> list:
        query_stems = [self.stemmer.stem(w.lower()) for w in query.split()]
        scores = defaultdict(int)

        for stem in query_stems:
            if stem in self.index:
                for item_idx in self.index[stem]:
                    item = self.raw_items[item_idx]
                    if stem in [self.stemmer.stem(w.lower()) for w in item['name'].split()]:
                        scores[item_idx] += 3
                    else:
                        scores[item_idx] += 1

        sorted_indices = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [self.raw_items[i] for i, score in sorted_indices]