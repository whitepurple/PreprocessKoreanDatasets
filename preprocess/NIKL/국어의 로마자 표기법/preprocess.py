import zipfile
from pathlib import Path
import json
from tqdm import tqdm
import pandas as pd
from datetime import datetime

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
        new_filename = file.with_suffix('.jsonl').name
        if 'Validation' in file.absolute().__str__():
            new_file = (valid_newdatadir/new_filename)
        else:
            new_file = (train_newdatadir/new_filename)
        print(new_file)
        if 'xlsx' in file.suffix:
            if new_file.exists():
                continue
            f = new_file.open('w')
            df = pd.read_excel(file)
            for _, row in tqdm(df.iterrows()):
                row = row.where(pd.notna(row), None).to_dict()
                row = {key: value.isoformat() if type(value) == datetime else value for key, value in row.items()}
                f.write(json.dumps(row, ensure_ascii=False)+'\n')
            f.close()


if __name__ == "__main__":
    main()
