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
            zip_file_list = sorted(zip_ref.namelist())
            for zip_file in tqdm(zip_file_list):
                with zip_ref.open(zip_file) as zip_data:
                    if zip_file.endswith('.json'):
                        data = zip_data.read()
                        raw_data = json.loads(data)
                        if 'data' in raw_data:
                            for rd in raw_data['data']:
                                f.write(json.dumps(rd, ensure_ascii=False)+'\n')
                        else:
                            f.write(json.dumps(raw_data, ensure_ascii=False)+'\n')
                    elif zip_file.endswith('.nt'):
                        data = zip_data.readlines()
                        for line in data:    
                            if not line or line.decode('utf-8').startswith("#"):
                                continue
                            line = line.strip()
                            entity, attribute, value, _ = line.split(maxsplit=3)
                            relation = {'entity': entity.decode('utf-8'), 
                                        'attribute': attribute.decode('utf-8'), 
                                        'value': value.decode('utf-8').replace('\"', '')}
                            f.write(json.dumps(relation, ensure_ascii=False)+'\n')
            f.close()

if __name__ == "__main__":
    main()
