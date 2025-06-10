import os #파일 경로 다루기
import json #JSON 파일 입출력 위해해

def load_result(): #result.json 파일 함수
    path = os.path.join(os.path.dirname(__file__), "result.json") #현재 파일이 있는 폴더 경로 기준 result.json 경로 생성 
    with open(path, "r", encoding="utf-8") as f: #해당 파일을 읽기 모드로 열기기
        return json.load(f) #JSON 파일 안에 있는 딕셔너리 반환

def load_result2(): #위와 마찬가지지
    path = os.path.join(os.path.dirname(__file__), "result2.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
#이 부분의 코드는 생성형 AI로 짰습니다다
