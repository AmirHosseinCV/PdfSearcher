
# Installation
1. Download and install git from [here](https://git-scm.com/download/).
2. Download and install Python from [here](https://www.python.org/downloads/).

     __Note:__ Do not forget to check "add python to PATH"
4. Open CMD and run these commands:
```
git clone https://github.com/AmirHosseinCV/PdfSearcher.git
cd PdfSearcher
pip install -r requirements.txt
```
if you want to generate JSON files on your system, run this command, too:
```
pip install -r additional_packages.txt
```
# Usage
First, you should prepare a JSON file from your PDF using the `convert.py` script.

We highly recommend using Colab if you are using windows.
Open [this colab notebook](https://colab.research.google.com/drive/1hB5vsSZyyyX32f8i6TXzQRFXmWhQkwJb?usp=sharing) and follow steps. You'll download a JSON file at the end. Place it near your pdf.

Now go to the project folder and run this command:
```
python main.py --pdf "[PATH_TO_YOUR_PDF_FILE]"
```
Replace `[PATH_TO_YOUR_PDF_FILE]` with the path to your pdf file!


Now you can open  "https://localhost:8000/search" in your browser.