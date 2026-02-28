from nltk.stem import PorterStemmer
from dataManager.DataModels import Items

stemmer = PorterStemmer()

class SearchEngine:

    def __init__(self, item: Items):
        self.items = item.getItems()

    def search(self, query: str) -> list:
        itemScores = []
        queryWords = [stemmer.stem(word.lower()) for word in query.split()]

        for item in self.items:
            score = 0
            itemName = [stemmer.stem(word) for word in item["name"].lower().split()]
            itemTags = [stemmer.stem(tag.lower()) for tag in item["tags"]]

            for word in queryWords:
                if word in itemName:
                    score += 2
                if word in itemTags:
                    score += 1

            if score > 0:
                itemScores.append((score, item))

        itemScores.sort(key=lambda x: x[0], reverse=True)

        return [item for score, item in itemScores]