from rank_bm25 import BM25Okapi
from PersianStemmer import PersianStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class BM25:
    def __init__(self):
        self.engine = None
        self.documents = []
        self.groups = []
        self.stemmer = PersianStemmer()

    def feed(self, docs, group=True):
        self.documents = docs if not group else [d[0] for d in docs]
        self.engine = BM25Okapi(self.tokenize(self.documents))
        if not group:
            self.groups = list(range(len(docs)))
        else:
            self.groups = [x[1] for x in docs]

    def find(self, query, n=5, custom_keys=None):
        scores = self.engine.get_scores(self.tokenize(query))
        if custom_keys is None:
            custom_keys = list(range(len(self.documents)))
        result = [[s, d, k, g] for s, d, k, g in zip(scores, self.documents, custom_keys, self.groups)]
        result.sort(key=lambda x: x[0], reverse=True)
        added_groups = set()
        filtered_results = []
        for r in result:
            if r[3] not in added_groups:
                filtered_results.append(r)
                added_groups.add(r[3])
        return [r[:] for r in filtered_results[:n]]

    @staticmethod
    def clear_text(text):
        for x in ")(?.!:;/\\{}&%$#-_'\"+*\u200e\t\n؟،»«۱۲۳۴۵۶۷۸۹۰0987654321" + "‌":
            text = text.replace(x, " ")
        for x in "ًٌٍَُِّ":
            text = text.replace(x, "")

        for key, val in dict({"آ": "ا", "أ": "ا", "ي": "ی", "ة": "ه", "ؤ": "و"}).items():
            text = text.replace(key, val)

        text = " ".join(text.split())

        return text

    def stem(self, text):
        return " ".join(self.stemmer.run(word) for word in text.split())

    def tokenize(self, text):
        if type(text) is list:
            return [self.stem(BM25.clear_text(t)).split(" ") for t in text]
        else:
            return self.stem(BM25.clear_text(text)).split(" ")


class TFIDF:
    def __init__(self):
        self.engine = TfidfVectorizer()
        self.documents = []
        self.vectorized_documents = []
        self.groups = []
        self.stemmer = PersianStemmer()

    def feed(self, docs, group=True):
        self.documents = docs if not group else [d[0] for d in docs]
        self.engine.fit([' '.join(self.tokenize(doc)) for doc in self.documents])
        self.vectorized_documents = self.engine.transform([' '.join(doc) for doc in self.tokenize(self.documents)])
        if not group:
            self.groups = list(range(len(docs)))
        else:
            self.groups = [x[1] for x in docs]

    def find(self, query, n=5, custom_keys=None):
        scores = cosine_similarity(self.engine.transform([query]), self.vectorized_documents)  # (1, n)
        scores = scores[0]
        if custom_keys is None:
            custom_keys = list(range(len(self.documents)))
        result = [[s, d, k, g] for s, d, k, g in zip(scores, self.documents, custom_keys, self.groups)]
        result.sort(key=lambda x: x[0], reverse=True)
        added_groups = set()
        filtered_results = []
        for r in result:
            if r[3] not in added_groups:
                filtered_results.append(r)
                added_groups.add(r[3])
        return [r[:] for r in filtered_results[:n]]

    @staticmethod
    def clear_text(text):
        for x in ")(?.!:;/\\{}&%$#-_'\"+*\u200e\t\n؟،»«۱۲۳۴۵۶۷۸۹۰0987654321" + "‌":
            text = text.replace(x, " ")
        for x in "ًٌٍَُِّ" + "ّ":
            text = text.replace(x, "")

        for key, val in dict({"آ": "ا", "أ": "ا", "ي": "ی", "ة": "ه", "ؤ": "و"}).items():
            text = text.replace(key, val)

        text = " ".join(text.split())

        return text

    def stem(self, text):
        return " ".join(self.stemmer.run(word) for word in text.split())

    def tokenize(self, text):
        if type(text) is list:
            return [self.stem(TFIDF.clear_text(t)).split(" ") for t in text]
        else:
            return self.stem(TFIDF.clear_text(text)).split(" ")
