from data import *
from inputall import *
from random import random,shuffle

result={num:{sub:"X" for sub in apply[num]} for num in apply} #시간 구간 표시 #학생 기준
result2={name:{} for name in subject} #선생님 기준

def sortkey(time,to,num): #쉬는시간 정렬에 대해 거리 고려
    #쉬는시간에 따라 그 전 수업과 후 수업 위치를 받아 거리합을 계산
    if 1<=time<=5: #1교시 시작 전으로 후 수업까지 거리*2로 계산
        return dist(place_sub[tt[int(num[1])][today][0]],to)*2
    elif 7<=time<=9:
        tcl=(0,1)
    elif 11<=time<=13:
        tcl=(1,2)
    elif 15<=time<=17:
        tcl=(2,3)
    elif 40<=time<=42:
        tcl=(4,5)
    elif 44<=time<=46:
        tcl=(5,6)
    return dist(place_sub[tt[int(num[1])][today][tcl[0]]],to)+dist(place_sub[tt[int(num[1])][today][tcl[1]]],to)

def sortkey2(sub,li): #학생이 정한 과목에 대한 우선순위 고려 
    i=li.index(sub)
    if i==0: return 0
    elif i==1: return 400
    elif i==2: return 500
    elif i==3: return 550

def sortall(): 
    #쉬는시간
    for j in teacher:
        for i in time_slot:
            if 19<=i<=38 or i not in time2[j]: continue
            my_place=teacher[j]
            applied=[(m[0],sortkey(i,my_place,m[0])+sortkey2(subject[j],m[1])) #학번과 점수를 반환(점수 낮으면 선정)\
                    for m in apply.items() if subject[j] in m[1] and #특정 선생님이 필요한 과목의 존재여부 확인\
                    subject[j] not in [i[0] for i in done_sub[m[0]]] and #이미 배정된 과목이 있는 경우 제외\
                    all(i+k not in [i[1] for i in done_sub[m[0]]] for k in range(-1,2))] #이미 그 시간이 차있지 않은지 확인
            if len(applied)==0: continue
            shuffle(applied) #점수가 같을 경우 학번순으로 되는 것 방지
            part=min(applied,key=lambda x:x[1])
            if sortkey(i,my_place,part[0])>=1060: continue #거리가 너무 멀 경우 가장 적합하더라도 제외
            done_sub[part[0]].append((subject[j],i))
            result[part[0]][subject[j]]=time_slot[i]
            result2[j][part[0]]=time_slot[i]
    #time_slot의 19~38은 점심시간에 해당, 위치 고려 안함
    #점심시간
    #쉬는 시간과 유사하지만 위치 고려X
    #변수 오류 떠서 다 다르게 변수 이름 고침
    for teacher_name in teacher:
        for slot in time_slot:
            if slot < 19 or slot > 38 or slot not in time2[teacher_name]:
                continue

            candidates = []
            for student_id, apps in apply.items():
                ds = done_sub[student_id]        
                assigned_periods = [p for (_, p) in ds] 

                if subject[teacher_name] in apps \
                    and subject[teacher_name] not in [sub for (sub, _) in ds] \
                    and all(slot + d not in assigned_periods for d in (-1, 0, 1)):

                    score = sortkey2(subject[teacher_name], apps)
                    score += random()  
                    candidates.append((student_id, score))

            if candidates:
                chosen = min(candidates, key=lambda x: x[1])[0]
                done_sub[chosen].append((subject[teacher_name], slot))
                result[chosen][subject[teacher_name]] = time_slot[slot]
                result2[teacher_name][chosen]=time_slot[slot]
    #신청되지 않은 경우 공강시간에 배정
    #공강
    for i in range(1,9):
        if "공강" in tt[i][today]:
            t=tt[i][today].index("공강")
            for student in apply:
                if student[1]==str(i):
                    for sub in apply[student]:
                        if sub in [i[0] for i in done_sub[student]]: continue
                        if any(t in time1[j] for j in subject_teacher[sub][i]): #공강시간에 선생님이 수업이 없는지 확인
                            result[student][sub]="공강"
                            for j in subject_teacher[sub][i]: 
                                if t in time1[j]:
                                    result2[j][student]=tclass[t] #선생님은 교시의 시간을 저장
                            done_sub[student].append((sub,"공강"))