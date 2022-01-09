from pathlib import Path
from search import TFIDF, BM25
from flask import Flask, redirect, url_for, request, render_template, make_response
import argparse
from loguru import logger
import pandas as pd
import utils
import fitz


parser = argparse.ArgumentParser()
parser.add_argument("--pdf", required=True, type=str, help="path to pdf file")
parser.add_argument("--host", default="localhost", type=str)
parser.add_argument("--port", default=8000, type=int)
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
data_file = Path(args.pdf.replace(".pdf", ".csv"))
pdf = fitz.open(str(pdf_file))
data = pd.read_csv(str(data_file), sep="\t")
text_data = utils.csv_to_text(data, sep="line_num")
corpus = []
for g, t in text_data.items():
    lines = t.split("\n", maxsplit=-1)
    if len(lines) < LINES:
        corpus.append((" ".join(lines), g))
        continue
    for i in range(0, max(len(lines) - LINES, 1), LINES // 2):
        corpus.append((" ".join(lines[i:i + LINES]), g))

engine.feed(corpus)


# Flask Application #######################################################################
app = Flask(__name__)


@app.route("/")
def main_page():
    return redirect(url_for("home_search"))


@app.route("/search", methods=["GET", "POST"])
def home_search():
    if 'query' in request.values:
        query = request.values["query"]
        stemmed_query = engine.stem(query)
        result = engine.find(query, n=int(args.num_results))
        for r in result:
            for q in set(r[1].split()):
                if len(q) > 2 and engine.stemmer.run(q) in stemmed_query:
                    r[1] = r[1].replace(q, f"<b>{q}</b>")
        return render_template("results.html", results=result, ids=[r[2] for r in result],
                                     query=query)
    return render_template("index.html")


@app.route("/view")
def view():
    page = int(request.values["page"])
    cdf = data[data['page_num'] == page]
    words = utils.words_location(cdf, request.values['query'], stemmer=engine.stemmer.run,
                                 cleaner=engine.clear_text)
    return render_template("view.html", page=page, words=words,
                                 from_page=max(0, page - 2), to_page=min(page + 2, pdf.page_count),
                                 query=request.values['query'])


@app.route("/pdf")
def view_pdf():
    from_page = int(request.values['from'])
    from_page = max(0, from_page)
    to_page = int(request.values['to'])
    doc2: fitz.Document = fitz.open()
    doc2.insert_pdf(pdf, from_page=from_page, to_page=to_page)
    for page_num in range(doc2.page_count):
        cdf = data[data['page_num'] == page_num + from_page + 1]
        page: fitz.Page = doc2[page_num]
        width, height = page.mediabox_size
        words = utils.words_location(cdf, request.values['query'],
                                     stemmer=engine.stemmer.run,
                                     cleaner=engine.clear_text)
        for w in words:
            x1, y1, w, h = w
            x1 = int(x1 * width / 100)
            y1 = int(y1 * height / 100)
            x2 = x1 + int(w * width / 100)
            y2 = y1 + int(h * height / 100)
            page.add_highlight_annot(quads=fitz.Rect(x1, y1, x2, y2))

    result_bytes = doc2.write()
    response = make_response(result_bytes)
    response.headers['Content-type'] = "application/pdf"
    response.headers["Content-Disposition"] = "inline"
    response.headers["accept-ranges"] = "bytes"
    return response


if __name__ == "__main__":
    app.run(host=args.host, port=args.port, threaded=True, debug=False)
