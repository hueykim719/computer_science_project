
#기본 라이브러리 import
import streamlit as st 
import pandas as pd 
import datetime
import time
from website_GUI import load_result, load_result2 #website_GUI.py에서 두 함수 import
import smtplib
import random
from email.message import EmailMessage

#JSON 불러오기 함수
result = load_result()
result2 = load_result2()

correct_password = "1410" 

#rerun에 변하지 않는 세션 상태 변수 초기화화
if "variable" not in st.session_state:
    st.session_state["variable"] = 0
if "banned" not in st.session_state:
    st.session_state["banned"] = 0
if "chance" not in st.session_state:
    st.session_state["chance"] = 3
if "passed" not in st.session_state:
    st.session_state["passed"] = 0

#로그인 화면
if not st.session_state["variable"]:
    st.error("설곽인 판별 테스트")
    password = st.text_input("서울과학고에서 가장 귀여운 학생의 학번은? (사심)", type="password")
    st.write("안전한 비밀번호 이런게 뜰텐데... 그건 구글의 내장프로그램이여서 어쩔 수가 없어요ㅜㅜ")    
    st.write("입력은 정상적으로 됩니다")
    if st.button("login"):
        if password == correct_password:
            st.session_state["variable"] = 1 #로그인 성공시 메인 화면으로
            st.success("✅ 로그인 성공!") #이모티콘 생성형 AI로
            st.snow() #눈이 오는 효과
            time.sleep(3) #3초동안 효과 유지 후
            st.rerun() #다른 화면으로 넘어감감
        elif password:
            st.error("❌ 비밀번호가 틀렸습니다.") #이모티콘 생성형 AI로
            time.sleep(0.5) #적당한 시간 지난 후 사라지게
            st.rerun()
#재즈 음악 로드
with open("jazz.mp3", "rb") as audiofile: 
    audio1 = audiofile.read()
#메인 화면 (variable == 1)
if st.session_state["variable"] == 1:
    time.sleep(3)
    today = datetime.date.today().strftime("%Y-%m-%d")

#사이드바 UI
    st.sidebar.title("📅 오늘 날짜")
    st.sidebar.write(f"**{today}**")
    st.sidebar.write("나는 내가 빛나는 별인줄 알았어요")
    st.sidebar.write("한번도 의심한 적 없었죠")
    st.sidebar.write("몰랐어요 난 내가 벌레라는 것을")
    st.sidebar.success("**그래도 괜찮아 난 빛날 테니까**")
    st.sidebar.write("-황가람, 나는 반딧불")
    #음악 부분 UI
    st.write("여러분들의 원활한 이의신청을 기원하며")
    st.write("재즈 음악을 준비했습니다")
    st.audio(audio1, format="audio/mp3")
    #풍선 날아오는 이벤트
    if st.button("놀라운 일이 벌어질수도?"):
        st.balloons()

    #학생들 일정을 표로 만드는 함수 - 생성형 AI 사용
    def image_students(x):
        Datatable = pd.DataFrame(x, columns=["과목","이의신청 시간대"]) #요소 이름름
        Datatable.index = range(1, len(Datatable) + 1) #인덱스를 1부터터
        st.table(Datatable)

    #마찬가지
    def image_teachers(x):
        Datatable = pd.DataFrame(x, columns=["이의신청 학생","시간대"])
        Datatable.index = range(1, len(Datatable) + 1)
        st.table(Datatable)
    
    #학생과 교사 중 선택해 다르게 적용
    page = st.radio("학생/교사 여부", ["학생","교사"])
    if page in ("학생","교사"):
        if page == "학생":
            st.header("학생용")
            studentID = st.text_input("당신의 학번을 입력하세요")
            if studentID:  # 빈 문자열이 아니면 → 즉 입력이 있으면
                if studentID in result:
                    st.info('당신의 일정은:')
                    image_students(result[studentID])
                    st.success('공강 시 이의신청은 알아서 하세요 ^^~~')
                else:
                    st.warning("⚠️ 해당 학번이 존재하지 않습니다.")
        if page == "교사":
            st.header("교사용")
            name = st.text_input("성함을 입력해주세요")
            if name:
                if name in result2:
                    st.info('당신의 일정은:')
                    image_teachers(result2[name])
                else:
                    st.warning("⚠️ 해당 교사가 존재하지 않습니다.")
    #후술: banned 변수가 1이 되면 비밀의 방으로 들어가는 버튼 제거
    if st.session_state["banned"] == 0:
        if st.button("비밀의 방"):
            st.session_state["variable"] = 3
            st.rerun()
#비밀의 방 안안
if st.session_state["variable"] == 3:
    secret_password = st.text_input("그대는... 이 방에 들어올 수 있는가?", type="password")
    if st.button("뒤로"): #뒤로 가는 버튼
        st.session_state["variable"]=1
    if st.button("자격의 증명"): #누르면 시도 가능
        if secret_password == "하늘을 꿰뚫는 마음을 가지고 있다":
            st.session_state["passed"] = 1 #비밀번호 맞을 시 비밀의 방 입장 가능
            st.write("비밀의 방으로 입장 중")
            time.sleep(3)
            st.session_state["variable"] = 2
            st.rerun()
        else:
            st.warning("틀렸네") #틀릴 시 총 3번의 기화, 다 소진시 메인화면으로 돌아가고 버튼 사라짐
            if st.session_state["chance"] == 3: 
                st.write("바위 아래 작은 샘물도 흘러서")
                time.sleep(2)
            if st.session_state["chance"] == 2: 
                st.write("바다로 갈 뜻을 가지고 있고")
            time.sleep(2)
            if st.session_state["chance"] == 1:
                st.write("뜰 앞의 작은 나무도")
                time.sleep(2)
            if st.session_state["chance"] == 0:
                st.warning("그대는 이 방에 들어올 자격이 없네네")
                st.session_state["variable"] = 1                    
                st.session_state["banned"] = 1
            st.session_state["chance"] -= 1
            st.rerun()

if st.session_state["variable"] == 2: #비밀의 방 이중인증 화면
    if st.session_state.get("email_verified"): #이미 이메일이 인증되어 있다면 생략
        st.session_state["variable"] = 4
        st.rerun()
    if st.button("뒤로"):
     st.session_state["variable"]=1
    st.title("2중 인증")
    if "certification_number" not in st.session_state:
        st.session_state["certification_number"] = None
    if "email_verified" not in st.session_state: 
        st.session_state["email_verified"] = False
    if "code_sent" not in st.session_state:
        st.session_state["code_sent"] = False

    st.write("sshs.hs.kr로 끝나는 이메일이여야 합니다. (선생님들 입장 불가)")
    email = st.text_input("이메일 주소를 입력하세요")
    if st.button("인증"):
        if not email:
            st.warning("이메일을 먼저 입력해주세요.")
        elif not email.endswith("@sshs.hs.kr"): #학생 계정 아니면 입장 불가
            st.error(" sshs.hs.kr로 끝나는 이메일만 입력할 수 있습니다.")
        else: 
            code = str(random.randint(100000,999999)) #인증코드 랜덤 생성
            st.session_state["certification_number"] = code
            st.session_state["code_sent"] = True
            msg = EmailMessage()
            msg["Subject"] = "Streamlit 인증 코드"
            msg["From"] = "25016@sshs.hs.kr"
            msg["To"] = email
            msg.set_content(f"인증 번호: {code}")
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login("25016@sshs.hs.kr", "jdow lsdc jsar xtrz")  
            server.send_message(msg)
            server.quit()  #입력한 이메일로 인증번호 보내는 과정 - 생성형 AI

            st.success("인증번호 전송 완료")
            st.success("만약 없다면 스팸 메일 확인")
            time.sleep(2)
            st.rerun()

    if st.session_state["code_sent"] == True: #인증번호 전송시
        user_code = st.text_input("이메일로 받은 인증번호를 입력하세요")
        if st.button("입장하기"):
            if user_code == st.session_state["certification_number"]: #맞으면 입장
                st.success("비밀의 방으로 입장합니다.")
                st.session_state["email_verified"] = True  # ✅ 추가
                time.sleep(2)
                st.session_state["variable"] = 4
                st.rerun()
            else:
                st.error("인증 실패")
                st.rerun()
if st.session_state["variable"] == 4: #비밀의 방
    if st.button("뒤로"): #뒤로 누를시 인증 필요없게 
        st.session_state["variable"] = 1
        st.session_state["code_sent"] = False  
        st.session_state["certification_number"] = None
        st.rerun()
    st.write("안녕")
    st.image("special.jpg", caption="나는 너희의 사감선생님이야", use_container_width=True) #사진진