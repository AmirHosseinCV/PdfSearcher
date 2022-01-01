from pathlib import Path
from search import TFIDF, BM25
import flask
import json
import argparse
from loguru import logger


parser = argparse.ArgumentParser()
parser.add_argument("--pdf", required=True, type=str, help="path to pdf file")
parser.add_argument("--lines", default=4, type=int, help="Split page to n-line parts (for search results)")
parser.add_argument("--engine", default="tfidf", type=str,
                    help="Information Retrieval algorithm, can be \"tfidf\" or \"bm25\"")
parser.add_argument("--num-results", default=10, type=int, help="number of results to show")
args = parser.parse_args()

LINES = args.lines
engine = None
if args.engine == "tfidf":
    engine = TFIDF()
elif args.engine == "bm25":
    engine = BM25()
else:
    logger.error(f"Unrecognized engine {args.engine}")
    exit(1)


pdf_file = Path(args.pdf)
data_file = Path(args.pdf.replace(".pdf", ".json"))
data = json.loads(data_file.read_text(encoding='utf8'))
corpus = []
for g, t in data.items():
    lines = t.split("\n", maxsplit=-1)
    if len(lines) < LINES:
        corpus.append((" ".join(lines), g))
        continue
    for i in range(0, max(len(lines) - LINES, 1), LINES // 2):
        corpus.append((" ".join(lines[i:i + LINES]), g))

engine.feed(corpus)


# Flask Application #######################################################################
app = flask.Flask(__name__)


@app.route("/search", methods=["GET", "POST"])
def home_search():
    if 'query' in flask.request.values:
        query = flask.request.values["query"]
        stemmed_query = engine.stem(query)
        result = engine.find(query, n=int(args.num_results))
        for r in result:
            for q in set(r[1].split()):
                if len(q) > 2 and engine.stemmer.run(q) in stemmed_query:
                    r[1] = r[1].replace(q, f"<b>{q}</b>")
        return flask.render_template("results.html", results=result, ids=[r[2] for r in result],
                                     query=query)
    return flask.render_template("index.html")


@app.route("/view")
def view():
    page = int(flask.request.values["page"])
    return flask.render_template("view.html", page=page)


@app.route("/pdf")
def view_pdf():
    return flask.send_from_directory(pdf_file.parent, pdf_file.name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True)
