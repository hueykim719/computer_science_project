import pandas as pd

file_path = '이의신청 우선순위 시트 .xlsx' #이의신청 당일 시트를 엑셀 파일로 다운로드해서 업로드하면 된다.
df = pd.read_excel(file_path, sheet_name="이의신청", header=0)# 엑셀 파일에서 "이의신청"탭의 첫번쨰를 행으로 읽는다.

df.columns = df.columns.str.strip() 
df.columns = df.columns.str.replace("\n", "") 
df.columns = df.columns.str.replace(" ", "") #컬럼명에서 공백과 '\n'을 제거한다.

df.rename(columns={"이의신청": "학번"}, inplace=True)# 이의신청 탭을 학번으로 바꾼다.

df = df.dropna(axis=1, how="all")

df = df[df["학번"].apply(lambda x: str(x).isdigit())]# 학번을 int로 변환한다.

df["학번"] = df["학번"].astype(int)

df = df.iloc[:, [0, 2, 3, 4, 5]] # 이름을 제외하고 학번이랑 1,2,3,4순위만 받는다.
df.columns = ["학번", "1순위", "2순위", "3순위", "4순위"]

student_ws = "\n".join(
    f"{row['학번']}\n{row['1순위']} {row['2순위']} {row['3순위']} {row['4순위']}"
    for _, row in df.iterrows()
)#main.py에서 이용하기 위한 형식으로 출력한다.

print(student_ws)