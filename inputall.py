from data import *

apply={} #학생들 이의신청 과목
time1={} #선생님들 되는 교시
time2={} #선생님들 되는 시간
today=0
done_sub={}

def inputprime(): 
    global apply,time1,time2,today
    today=int(input("요일(월요일부터 0):"))
    maxpercl=int(input("각 반의 최대 인원:"))
    #학번과 신청된 과목 입력
    while True:
        num=input("학번(끝이면 end):")
        if num=="end":break
        if not (len(num)==4 and num[0]=="1" and "1"<=num[1]<="8" and "0"<=num[2]<="9" and "0"<=num[3]<="9" and int(num[2:4])<=maxpercl):
            print("유효하지 않은 학번입니다.")
            continue
        while True:
            app=input("과목 입력(4개까지):").split()
            if len(app)<=4 and all(i in subject_teacher.keys() for i in app):
                apply[num]=app
                done_sub[num]=[]
                break
            print("잘못 입력되었습니다.")
    for name in teacher:
        #첫번째는 쌤들 수업 없는 교시 받아서 time1에 넣어주고
        #8:50~10:20 1:20~3:20 이런식으로 적으면 그 시간대 안에 있는 time_slot 원소 다 선택되게
        print(name)
        #선생님 가능 교시 입력(공강시간 고려)
        while True:
            possclass=input("가능 교시:").split()
            if all(len(i)==1 and "1"<=i<="7" for i in possclass):
                time1[name]=list(map(lambda x:int(x)-1,possclass)) #교시 인덱싱으로 -1해야됨
                break
            print("잘못 입력되었습니다.")
        #시간대 입력하면 time_slot에서 가능한 시간 선정
        while True:
            posstime=input("가능 시간(ex. 8:50~10:20 1:20~3:20):").split()
            if all(timesplit.count("~")==1 and timesplit.count(":")==2 and all("0"<=i<="9" for i in timesplit if i not in {"~",":"," "}) for timesplit in posstime):
                time2[name]=list(filter(lambda x:any(betweentime(time.split("~")[0],time.split("~")[1],time_slot[x][:5]) for time in posstime),time_slot))
                break
            print("잘못 입력되었습니다.")
    for cl in range(1,9):  
        #1학년 시간표로 선생님 시간 역추적 후 제외
        for sub in range(len(tt[cl][today])):
            try:
                if tt[cl][today][sub]=="수학":
                    if sub==6 or tt[cl][today][sub+1]!="수학":
                        if cl<=4:
                            s="심영훈"
                        else:
                            s="길준영"
                    else:
                        if cl<=4:
                            s="양동규"
                        else:
                            s="김명식"
                elif tt[cl][today][sub]=="물리":
                    if 1<=cl<=3:
                        s="배동일"
                    elif 4<=cl<=6:
                        s="신다인"
                    else:
                        s="김상태"
                else:
                    s=class_teacher[tt[cl][today][sub]][cl]
                time1[s].remove(sub)
            except:
                continue