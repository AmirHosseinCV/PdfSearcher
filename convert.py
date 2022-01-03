from pathlib import Path
import argparse
import tqdm
from loguru import logger
from copy import deepcopy
import pandas as pd
import fitz
from PIL import Image
import io
import joblib


parser = argparse.ArgumentParser()
parser.add_argument("--pdf", type=str, required=True, help="path to the pdf file")
parser.add_argument("--ocr", type=int, default=1, choices=[1, 0], help="Use OCR (if pdf is not searchable)")
args = parser.parse_args()

OCR = args.ocr
pdf = Path(args.pdf)


doc = fitz.open(str(pdf))
logger.success(f"PDF loaded successfully ({doc.page_count} pages)")
df = None

if OCR:
    import pytesseract

    tesseract_config = '--tessdata-dir "./files/tessdata"'

    logger.info("Converting images to text...")
    logger.info(f"Using { joblib.cpu_count() } threads")

    dfs = []
    bar = tqdm.tqdm(total=doc.page_count)

    def run(i):
        page: fitz.fitz.Page = doc[i]
        img: fitz.fitz.Pixmap = page.get_pixmap(dpi=None)
        img = Image.open(io.BytesIO(img.tobytes()))
        current_df = pytesseract.image_to_data(img, lang='fas_fast', config=tesseract_config,
                                               output_type=pytesseract.Output.DATAFRAME)
        current_df['page_num'] = i + 1
        dfs.append(deepcopy(current_df))
        bar.update(1)
    joblib.Parallel(n_jobs=joblib.cpu_count(), backend='threading')(joblib.delayed(run)(i, ) for i in range(doc.page_count))
    bar.close()
    df = pd.concat(dfs)
    df = df.sort_values(by=['page_num', 'block_num', 'par_num', 'line_num', 'word_num'])
    logger.success("Done!")

else:
    logger.info("Converting...")
    data = []
    for i in range(doc.page_count):
        page = doc[i]
        words = page.get_textpage().extractWORDS()
        num_words = len(words)
        for w in words:
            (x0, y0, x1, y1, text, block_no, line_no, word_no) = w
            data.append(
                {
                    "page_num": i + 1,
                    "block_num": block_no,
                    "line_num": line_no,
                    "word_num": num_words - word_no,
                    "top": y0,
                    "left": x0,
                    "width": x1 - x0,
                    "height": y1 - y0,
                    "text": text[::-1]
                }
            )
        data.append(
            {
                "page_num": i + 1,
                "block_num": 0,
                "line_num": 0,
                "word_num": 0,
                "top": 0,
                "left": 0,
                "width": page.mediabox_size[0],
                "height": page.mediabox_size[1],
                "text": None
            }
        )
    data.sort(key=lambda x: (x['page_num'], x['block_num'], x['line_num'], x['word_num']))
    df = pd.DataFrame(data)
    logger.success("Done!")

df.to_csv(str((pdf.parent / (pdf.stem + ".csv"))), sep='\t', index_label='id')
logger.success(f'Output saved at {(pdf.parent / (pdf.stem + ".csv"))}')
