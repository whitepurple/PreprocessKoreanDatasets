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
        if file_path.is_file() and all(t not in file_path.stem for t in ['sample', 'preprocess']) and 'preprocess' not in str(file_path.absolute()):
            all_files.append(file_path)

    for file in all_files:
        new_filename = file.with_suffix('.jsonl').name
        if 'Validation' in file.absolute().__str__():
            new_file = (valid_newdatadir/new_filename)
        else:
            new_file = (train_newdatadir/new_filename)
        print(new_file)
        f = new_file.open('w')
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_file_list = sorted(zip_ref.namelist(), reverse=True)
            for zip_file in tqdm(zip_file_list):
                with zip_ref.open(zip_file) as zip_data:
                    data = zip_data.read()
                    if zip_file.endswith('.json'):
                        zip_file_dir = '/'.join(zip_file.split('/')[:-1])
                        if data:
                            raw_data = json.loads(data)['dataSet']
                    elif zip_file.endswith('.txt'):
                        if data:
                            text_data = data.decode('utf-8').strip().replace('n/ ', '').replace('b/ ', '')
                            if 'texts' in raw_data:
                                raw_data['texts'] = [text_data]+raw_data['texts']
                            else:
                                raw_data['texts'] = [text_data]
                    elif zip_file[:-1] == zip_file_dir:
                        f.write(json.dumps(raw_data, ensure_ascii=False)+'\n')
        f.close()

if __name__ == "__main__":
    main()
