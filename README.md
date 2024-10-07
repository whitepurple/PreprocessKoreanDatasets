# korean-data-to-jsonl
AIHub, 모두의 말뭉치 등 한국어 데이터셋의 JSONL 파일 포맷 전처리 저장소 입니다. \
Preprocesses Korean datasets from AIHub and Moducorpus into JSONL format 


## 데이터 접근 및 세팅
### 접근
본 저장소의 모든 데이터는 다음 소스에서 개별적으로 신청 후 접근할 수 있습니다. 
- [AI Hub 링크](https://aihub.or.kr/aihubdata/data/list.do?currMenu=115&topMenu=100)
- [모두의 말뭉치 링크](https://kli.korean.go.kr/corpus/main/requestMain.do?lang=ko)

### 세팅
1. 각 소스에 맞는 데이터셋을 다운로드 후, ```./data```에 위치. 혹은 ```settings.json```의 path 수정
2. ```./preprocess```의 ```source```와 ```datasetname``` 일치 확인 후 ```preprocess.py``` 실행
3. 동일 위치의 ```preprocess_task.ipynb``` 실행 (추후 수정 예정)

## 데이터 기록 Notion [[link](https://tropical-literature-93e.notion.site/118677e64fc4815dbed2c9eaef0d061b)]
각 데이터별 Task 및 세부사항은 위 Notion link에 기록됩니다. 

### History
- 2024.07.31 AIHub, 모두의 말뭉치, 국립국어원(NIKL) 갱신
- 2024.10.07 Repo 정리


## 데이터 전처리

AI Hub와 모두의 말뭉치에서 한국어 LLM에 사용할 수 있는 데이터셋을 수집하고, 
이 데이터셋의 구조를 그대로 유지하여 jsonl 형식으로 전처리합니다.
데이터셋별 Task를 식별하여 필요한 요소만 남겨 다시 전처리합니다. 

[데이터 리스트 및 규모](./jsonl_file_sizes.txt)

## TODO List

- [X] 데이터셋 수집
- [X] 데이터셋 구조 분석
- [X] JSONL 형식으로 전처리
- [X] 데이터셋별 Task 식별
- [X] Task별 전처리
- [ ] Task별 포맷 통일 - **ongoing**
- [ ] notebook file 정리 - **ongoing**
- [ ] Task, Sample 별 Instruction format 생성
