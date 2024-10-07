import zipfile
from pathlib import Path
import json
from tqdm import tqdm
import pandas as pd
import io


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
            new_file = (valid_newdatadir/new_filename)
        else:
            new_file = (train_newdatadir/new_filename)
        print(file)
        f = new_file.open('w')
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_file_list = zip_ref.namelist()
            # print(zip_file_list)
            for zip_file in tqdm(zip_file_list):
                with zip_ref.open(zip_file) as zip_data:
                    extract_file = zip_ref.extract(zip_file, newdatadir)
                    ef = Path(newdatadir/extract_file).open('r')
                    edit_file = []
                    edit_file.append(ef.readline().replace('"', ''))
                    ef.readline()
                    edit_file.extend(ef.readlines())
                    # print(edit_file[:10])
                    df = pd.read_csv(io.StringIO(''.join(edit_file)))
                    for _, row in tqdm(df.iterrows()):
                        # NaN to null
                        row = row.where(pd.notna(row), None)
                        f.write(json.dumps(row.to_dict(), ensure_ascii=False)+'\n')
        f.close()


if __name__ == "__main__":
    main()
