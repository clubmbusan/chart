import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# 제목 설정
st.title("금 시세 변화 차트")
st.write("아래 선택 메뉴를 사용하여 일별, 월별, 연별 금 시세를 확인할 수 있습니다.")

# 사용자 입력을 받는 Selectbox (기본값: 월별 시세)
option = st.selectbox(
    "원하는 기간을 선택하세요:",
    ["일별 시세", "월별 시세", "연별 시세"],
    index=1  # 기본값으로 '월별 시세' 선택
)

# 실시간 데이터 가져오기 (GLD: SPDR Gold ETF 사용)
ticker = "GLD"
data = yf.download(ticker, period="5y", interval="1d")  # 최근 5년 데이터 가져오기
data.reset_index(inplace=True)

# 일별, 월별, 연별 데이터 준비
data["날짜"] = data["Date"]
data["월"] = data["Date"].dt.to_period("M").dt.to_timestamp()  # 월별 기준
data["연"] = data["Date"].dt.to_period("Y").dt.to_timestamp()  # 연별 기준

# 옵션에 따라 데이터 필터링
if option == "일별 시세":
    filtered_data = data[["날짜", "Close"]]
    x_axis = filtered_data["날짜"]
    y_axis = filtered_data["Close"]
    title = "일별 금 시세 차트"

elif option == "월별 시세":
    filtered_data = data.groupby("월")["Close"].mean().reset_index()
    x_axis = filtered_data["월"]
    y_axis = filtered_data["Close"]
    title = "월별 금 시세 차트"

elif option == "연별 시세":
    filtered_data = data.groupby("연")["Close"].mean().reset_index()
    x_axis = filtered_data["연"]
    y_axis = filtered_data["Close"]
    title = "연별 금 시세 차트"

# Plotly 차트 생성
fig = go.Figure()
fig.add_trace(go.Scatter(x=x_axis, y=y_axis, mode="lines+markers", name=title))
fig.update_layout(title=title, xaxis_title="기간", yaxis_title="가격 (USD)")

# 차트 출력
st.plotly_chart(fig)

# 추가 메시지
st.write("이 데이터는 SPDR Gold Shares ETF (GLD)의 시세를 기반으로 합니다.")
