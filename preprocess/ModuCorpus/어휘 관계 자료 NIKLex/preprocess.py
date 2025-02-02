import zipfile
from pathlib import Path
import json
from tqdm import tqdm
import pandas as pd

def main():
    settings = json.loads(Path('settings.json').read_text())
    raw_data_path = Path(settings['raw_data_path'])
    preprocessed_data_path = Path(settings['preprocessed_data_path'])
    data_path = Path(__file__).resolve().parent
    data_name = data_path.name
    source_name = data_path.parent.name
    
    raw_dir = raw_data_path/source_name/data_name
    preprocessed_dir = preprocessed_data_path/source_name/data_name
    
    newdatadir = preprocessed_dir/'preprocessed'
    train_newdatadir = newdatadir/'train'
    valid_newdatadir = newdatadir/'valid'
    train_newdatadir.mkdir(parents=True, exist_ok=True)
    valid_newdatadir.mkdir(parents=True, exist_ok=True)

    all_files = []
    for file_path in raw_dir.glob('**/*'):
        if file_path.is_file() and all(t not in file_path.stem for t in ['sample', 'preprocess']) and 'preprocess' not in str(file_path.absolute()):
            all_files.append(file_path)

    for file in all_files:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_file_list = zip_ref.namelist()
            for zip_file in tqdm(zip_file_list):
                if 'tsv' in zip_file:
                    new_filename = Path(zip_file).with_suffix('.jsonl').name
                    if 'Validation' in file.absolute().__str__():
                        new_file = (valid_newdatadir/new_filename)
                    else:
                        new_file = (train_newdatadir/new_filename)
                    f = new_file.open('w')
                    
                    with zip_ref.open(zip_file) as zip_data:
                        df = pd.read_csv(zip_data, sep='\t')
                        for _, row in tqdm(df.iterrows()):
                            row = row.where(pd.notna(row), None)
                            f.write(json.dumps(row.to_dict(), ensure_ascii=False)+'\n')
                    f.close()
                elif 'pdf' in zip_file:
                    pdf_file = zip_ref.extract(zip_file, newdatadir)
                    Path(pdf_file).rename(newdatadir/Path(zip_file.encode('cp437').decode('cp949')).name)
                    try:
                        Path(pdf_file).parent.rmdir()
                    except:
                        continue
                


if __name__ == "__main__":
    main()
