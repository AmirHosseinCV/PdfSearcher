from pathlib import Path
import argparse
import tqdm
from loguru import logger
import json

parser = argparse.ArgumentParser()
parser.add_argument("--pdf", type=str, required=True, help="path to the pdf file")
parser.add_argument("--ocr", type=int, default=1, choices=[1, 0], help="Use OCR (if pdf is not searchable)")
args = parser.parse_args()

OCR = args.ocr
pdf = Path(args.pdf)

output = pdf.parent / (pdf.stem + "-data")
if output.exists():
    output.rmdir()
output.mkdir()

data = {}

if OCR:
    import tempfile
    import pytesseract
    import pdf2image

    tesseract_config = '--tessdata-dir "./files/tessdata" --dpi 200'

    with tempfile.TemporaryDirectory() as path:

        logger.info("Converting PDF to images...")
        image_files = pdf2image.convert_from_path(str(pdf),
                                                  paths_only=True,
                                                  output_folder=path)
        logger.success("Done!")
        logger.info("Converting images to text...")
        bar = tqdm.tqdm(total=len(image_files))
        for i, img in enumerate(image_files):
            s = pytesseract.image_to_string(img, lang='fas_fast', config=tesseract_config)
            data[str(i + 1)] = s
            bar.update(1)
        bar.close()
        logger.success("Done!")

else:
    import pdfplumber
    pages = pdfplumber.open(str(pdf)).pages
    logger.success(f"PDF loaded successfully ({len(pages)} pages)")
    logger.info("Converting...")
    for i in range(len(pages)):
        page = pages[i]
        page_text = page.extract_text()
        lines = []
        for line in page_text.split("\n"):
            result = []
            for w in line.split():
                result.append(w[::-1])
            result.reverse()
            lines.append(' '.join(result))
        page_text_rtl = "\n".join(lines)
        data[str(i + 1)] = page_text_rtl
    logger.success("Done!")

(pdf.parent / (pdf.stem + ".json")).write_text(json.dumps(data), encoding='utf8')
logger.success(f'Output saved at {(pdf.parent / (pdf.stem + ".json"))}')
