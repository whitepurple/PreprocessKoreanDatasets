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
        new_filename = file.with_suffix('.jsonl').name
        if 'Validation' in file.absolute().__str__():
            new_file = (valid_newdatadir/new_filename)
        else:
            new_file = (train_newdatadir/new_filename)
        print(new_file)
        f = new_file.open('w')
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_file_list = zip_ref.namelist()
            for zip_file in tqdm(zip_file_list):
                # 
                if 'csv' in zip_file:
                    new_filename = Path(zip_file).with_suffix('.jsonl').name
                    if 'Validation' in file.absolute().__str__():
                        new_file = (valid_newdatadir/new_filename)
                    else:
                        new_file = (train_newdatadir/new_filename)
                    f = new_file.open('w')
                    
                    with zip_ref.open(zip_file) as zip_data:
                        df = pd.read_csv(zip_data)
                        for _, row in tqdm(df.iterrows()):
                            row = row.where(pd.notna(row), None)
                            f.write(json.dumps(row.to_dict(), ensure_ascii=False)+'\n')
                    f.close()
                elif 'pdf' in zip_file:
                    pdf_file = zip_ref.extract(zip_file, newdatadir)
                    Path(pdf_file).rename(newdatadir/Path(zip_file.encode('utf-8').decode('utf-8')).name)
                    try:
                        Path(pdf_file).parent.rmdir()
                    except:
                        continue
        f.close()
        
def xml_to_json(element):
    json_data = {}
    
    # 요소의 속성을 JSON으로 추가
    if element.attrib:
        json_data.update(element.attrib)
    
    # 하위 요소를 재귀적으로 탐색하여 JSON으로 추가
    for child in element:
        # 요소의 텍스트를 JSON으로 추가
        if child.text and child.text.strip():
            json_data[child.tag] = child.text.strip()
        else:
            child_data = xml_to_json(child)
            tag = child.tag
        
            # 중복된 태그 처리
            if tag in json_data:
                if isinstance(json_data[tag], list):
                    json_data[tag].append(child_data)
                else:
                    json_data[tag] = [json_data[tag], child_data]
            else:
                if child_data:
                    json_data[tag] = child_data
                else:
                    json_data[tag] = None
    
    return json_data


if __name__ == "__main__":
    main()
