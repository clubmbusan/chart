import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 제목
st.title("금 시세 변화 차트")
st.write("아래 선택 메뉴를 사용하여 일별, 월별, 연별 금 시세를 확인하세요.")

# 가상의 데이터 생성 (2024년 기준)
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
daily_prices = np.cumsum(np.random.randn(len(dates))) + 1800  # 기본값 1800에서 랜덤 변화

data = pd.DataFrame({"날짜": dates, "가격": daily_prices})
data["월"] = data["날짜"].dt.to_period("M").dt.to_timestamp()
data["연"] = data["날짜"].dt.to_period("Y").dt.to_timestamp()

# 사용자 입력
option = st.selectbox(
    "원하는 기간을 선택하세요:",
    ["2024년 일별 시세", "2024년 월별 시세", "연별 시세"]
)

# 옵션별 데이터 처리
if option == "2024년 일별 시세":
    x_axis = data["날짜"]
    y_axis = data["가격"]
    title = "2024년 일별 금 시세 변화"

elif option == "2024년 월별 시세":
    monthly_data = data.groupby("월")["가격"].mean().reset_index()
    x_axis = monthly_data["월"]
    y_axis = monthly_data["가격"]
    title = "2024년 월별 금 시세 변화"

elif option == "연별 시세":
    yearly_data = data.groupby("연")["가격"].mean().reset_index()
    x_axis = yearly_data["연"]
    y_axis = yearly_data["가격"]
    title = "연별 금 시세 변화"

# Plotly 차트 생성
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x_axis, 
    y=y_axis, 
    mode="lines+markers",
    line=dict(color="blue", width=2),
    name=title
))

fig.update_layout(
    title=title,
    xaxis_title="기간",
    yaxis_title="가격 (USD)",
    template="plotly_white"
)

# 차트 출력
st.plotly_chart(fig)

# 데이터 출처 표시
st.write("이 데이터는 가상의 데이터입니다. 실제 시세가 아닙니다.")
