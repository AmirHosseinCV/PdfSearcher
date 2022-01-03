# Installation
## Required
1. Download and install git from [here](https://git-scm.com/download/).
2. Download and install Python from [here](https://www.python.org/downloads/).

    __Note:__ Do not forget to check "add python to PATH".
3. Open CMD and run the following commands:
```
git clone https://github.com/AmirHosseinCV/PdfSearcher.git
cd PdfSearcher
pip install --prefer-binary -r requirements.txt
```
## Optional
If you want to generate CSV files on your system, do the steps below:
1. Run the following command in the project folder:
```
pip install -r additional_packages.txt
```
2. Download and install MSYS2 from [here](https://www.msys2.org/).

3. Open MSYS2 terminal and run these commands (each command might ask for your confirmation, type 'Y' and press ENTER)
```
pacman -Syu
pacman -S mingw-w64-x86_64-tesseract-ocr
```
# Usage
## Step 1: prepare a CSV file:
### Option 1 (Recommended)
First, you should prepare a CSV file from your PDF using the `convert.py` script. This file contains the locations of all words in your PDF.

We highly recommend using Colab if you are using windows.
Open [this Colab notebook](https://colab.research.google.com/drive/1hB5vsSZyyyX32f8i6TXzQRFXmWhQkwJb?usp=sharing) and follow steps. You'll download a CSV file at the end. Place it near your PDF.

### Option 2
__Note: you can't run the following command if you don't have tesseract installed.__

If you want to prepare CSV files on your system, go to the project folder (which contains convert.py) and run the following command (if you don't want to use ocr, change its value from 1 to 0):
```
python convert.py --pdf "[PATH_TO_YOUR_PDF_FILE]" --ocr 1
```
## Step 2: Run the program
After placing the CSV file near your PDF file, in the project folder __(which contains main.py file)__ run this command:
```
python main.py --pdf "[PATH_TO_YOUR_PDF_FILE]"
```
Replace `[PATH_TO_YOUR_PDF_FILE]` with the path to your pdf file!
For example
```
python main.py --pdf "C:\path\to\file.pdf"
```

After that, you'll be able to open "https://localhost:8000/search" in your browser.
