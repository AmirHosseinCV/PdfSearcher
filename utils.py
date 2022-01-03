import pandas as pd


def csv_to_text(df: pd.DataFrame, sep="par_num", word_column="text", page_column="page_num"):
    result = {}
    pages = set(df[page_column].values)
    for page in pages:
        cdf = df[df[page_column] == page]
        text = ""
        prev_line = -1
        words_count = 0
        for k, row in cdf.iterrows():
            if row[sep] != prev_line:
                prev_line = row[sep]
                if words_count > 0:
                    text += "\n"
                words_count = 0
            if not row.hasnans:
                text += str(row[word_column]) + " "
                words_count += 1
        result[page] = text
    return result


def search(x, p, cleaner=None, stemmer=None):
    if type(x) == float:
        return False
    if not stemmer or not cleaner:
        for x1 in p.split():
            if x == x1:
                return True
    else:
        x = cleaner(stemmer(x))
        for x1 in p.split():
            if x == cleaner(stemmer(x1)):
                return True
    return False


def words_location(df: pd.DataFrame, phrase, words_column="text", cleaner=None, stemmer=None):
    width = df['width'].max()
    height = df['height'].max()
    results = []
    found = df[df[words_column].apply(search, args=(phrase, cleaner, stemmer))]
    for i in range(len(found)):
        row = found.iloc[i]
        l, t, w, h = row['left'] / width, row['top'] / height, row['width'] / width, row['height'] / height
        l, t, w, h = l * 100, t * 100, w * 100, h * 100
        results.append([l, t, w, h])
    return results
