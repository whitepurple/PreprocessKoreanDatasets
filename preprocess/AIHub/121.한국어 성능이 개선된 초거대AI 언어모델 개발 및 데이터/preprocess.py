from base64 import encode
import zipfile
from pathlib import Path
import json
from tqdm import tqdm

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
        if file_path.is_file() and file_path.stem not in ['sample', 'preprocess'] and 'preprocess' not in str(file_path.absolute()):
            all_files.append(file_path)
    
    for file in all_files:
        new_filename = file.with_suffix('.jsonl').name
        if 'Validation' in file.absolute().__str__():
            data_type = 'val'
            new_file = (valid_newdatadir/new_filename)
        elif 'Other' in file.absolute().__str__():
            data_type = 'other'
            new_file = (train_newdatadir/new_filename)
        else:
            data_type = 'train'
            new_file = (train_newdatadir/new_filename)
        print(new_file)
        f = new_file.open('w')
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_file_list = zip_ref.namelist()
            for zip_file in tqdm(zip_file_list):
                if data_type == 'train':
                    if 'json' in zip_file and 'TS_02' not in zip_file:
                        with zip_ref.open(zip_file) as zip_data:
                            data = zip_data.read()
                            if data:
                                raw_data = json.loads(data)['data_info']
                                for rd in raw_data:
                                    f.write(json.dumps(rd, ensure_ascii=False)+'\n')
                    
                elif data_type == 'val':
                    if 'json' in zip_file and 'VS_02' not in zip_file:
                        with zip_ref.open(zip_file) as zip_data:
                            data = zip_data.read()
                            if data:
                                raw_data = json.loads(data)['data_info']
                                for rd in raw_data:
                                    f.write(json.dumps(rd, ensure_ascii=False)+'\n')
                    
                if data_type == 'other':                
                    if 'json' in zip_file:
                        with zip_ref.open(zip_file) as zip_data:
                            data = zip_data.read()
                            if data:
                                raw_data = json.loads(data)
                                for rd in raw_data:
                                    f.write(json.dumps(rd, ensure_ascii=False)+'\n')
        f.close()
    
if __name__ == "__main__":
    main()