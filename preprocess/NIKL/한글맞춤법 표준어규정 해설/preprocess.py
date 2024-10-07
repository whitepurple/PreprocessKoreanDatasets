from PyPDF2 import PdfReader
import re
from pathlib import Path
from tqdm import tqdm
import json

def pdf_to_text(pdf_path, txt_path):
    rawdatadir = Path(__file__).resolve().parent
    newdatadir = rawdatadir/'preprocessed'
    train_newdatadir = newdatadir/'train'
    valid_newdatadir = newdatadir/'valid'
    train_newdatadir.mkdir(parents=True, exist_ok=True)
    valid_newdatadir.mkdir(parents=True, exist_ok=True)
    
    with open(rawdatadir/pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        
        with open(train_newdatadir/txt_path, 'w', encoding='utf-8') as txt_file:
            num_pages = len(pdf_reader.pages)
            total_text = ''
            for page_num in tqdm(range(num_pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text = re.sub(r'Ⅰ\.‘한글 맞춤법 ’ 해설[^가-힣0-9a-zA-Z\-\(\)\[\]\.\,]+', ' ', text)
                text = re.sub(r'‘한글 맞춤법 ’, ‘표준어 규정’ 해설 [^가-힣0-9a-zA-Z\-\(\)\[\]\.\,]+', ' ', text)
                text = re.sub(r'Ⅱ\.‘표준어 규정’ 해설[^가-힣0-9a-zA-Z\-\(\)\[\]\.\,]+', ' ', text)
                text = text.replace('다 .', '다.')
                text = re.sub(r'(?<=제\d)항(?=.)', '항 ', text)
                text = re.sub(r'(?<=제\d\d)항(?=.)', '항 ', text)
                text = re.sub(r'(?<=[^ ].)제(?=\d+[절항])', ' 제', text)
                text = re.sub(r'(?<=[‘\(\[]) ', '', text)
                text = re.sub(r' (?=[’\)\]\,])', '', text)
                text = re.sub(r'(?<=[^\.])\n', '', text)
                text = text.replace('\n', ' ')
                text = re.sub(r'[· ]+', ' ', text)
                
                total_text += text
            
            for text in total_text.split('\n'):
                txt_file.write(json.dumps({'text': text}, ensure_ascii=False)+'\n')


if __name__ == "__main__":
    pdf_path = "한글맞춤법+표준어규정+해설.pdf"
    txt_path = "한글맞춤법+표준어규정+해설.jsonl"

    pdf_to_text(pdf_path, txt_path)