import json
from data import *
from inputall import *

inputprime()  #입력

from algrthm import * #모듈 내 input 부분이 필요한 부분이 있어 나중에 import

sortall()  #시간별로 정렬된 result, result2 반환(dictionary)
result={i:list(map(list,j.items())) for i,j in result.items()}  #json으로 파일을 저장하기 위해 리스트로 변환
result2={i:sorted(j.items(),key=lambda x:x[1][:5].split(':')) for i,j in result2.items()} #시간에 대해 정렬된 리스트로 변환

#파일저장
with open("result.json","w",encoding="utf-8") as f:
    json.dump(result,f,ensure_ascii=False,indent=4)
with open("result2.json","w",encoding="utf-8") as f:
    json.dump(result2,f,ensure_ascii=False,indent=4)