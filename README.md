# Installation
1. Download and install git from [here](https://git-scm.com/download/).
2. Download and install Python from [here](https://www.python.org/downloads/).

    __Note:__ Do not forget to check "add python to PATH".
3. Download and install the latest version of tesseract from [here](https://digi.bib.uni-mannheim.de/tesseract/) (Scroll to the end of the page. Currently the latest version is [ tesseract-ocr-w64-setup-v5.0.1.20220107.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.1.20220107.exe))
4. Open CMD and run the following commands:
```
git clone https://github.com/AmirHosseinCV/PdfSearcher.git
cd PdfSearcher
pip install --prefer-binary -r requirements.txt
```
# Usage
## Step 1: prepare a CSV file
You need a CSV file that contains the locations of all words in your PDF file.

To prepare this file, go to the project folder (which contains convert.py) and run the following command (if you don't want to use ocr, change its value from 1 to 0):
```
python convert.py --pdf "[PATH_TO_YOUR_PDF_FILE]" --ocr 1
```
Use `python convert.py --help` for more information.
## Step 2: Run the program
After placing the CSV file near your PDF file, run the following command in the project folder __(which contains main.py file)__:
```
python main.py --pdf "[PATH_TO_YOUR_PDF_FILE]"
```
The PDF and CSV files must be in the same directory and have the same name.

Replace `[PATH_TO_YOUR_PDF_FILE]` with the path to your pdf file! Use `python main.py --help` for more information.

After that, you'll be able to open "https://localhost:8000/search" in your browser.
