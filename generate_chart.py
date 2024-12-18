import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# 제목
st.title("금 시세 변화 차트")
st.write("아래 선택 메뉴를 사용하여 일별, 월별, 연별 금 시세를 확인하세요.")

# 데이터 다운로드 - 2024년만 가져오기
ticker = "GLD"  # SPDR Gold ETF
st.write("데이터 다운로드 중...")
try:
    data = yf.download(ticker, start="2024-01-01", end="2024-12-31", interval="1d")
    st.write("데이터 미리보기:", data.head())
except Exception as e:
    st.error(f"데이터를 가져오는 중 오류 발생: {e}")

# 데이터 확인
if data.empty:
    st.error("데이터가 비어 있습니다. yfinance에서 데이터를 가져오지 못했습니다.")
else:
    st.success("데이터가 정상적으로 다운로드되었습니다.")

# 날짜 처리
data.reset_index(inplace=True)
data["날짜"] = pd.to_datetime(data["Date"])
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
    y_axis = data["Close"]
    title = "2024년 일별 금 시세 변화"

elif option == "2024년 월별 시세":
    monthly_data = data.groupby("월")["Close"].mean().reset_index()
    x_axis = monthly_data["월"]
    y_axis = monthly_data["Close"]
    title = "2024년 월별 금 시세 변화"

elif option == "연별 시세":
    yearly_data = data.groupby("연")["Close"].mean().reset_index()
    x_axis = yearly_data["연"]
    y_axis = yearly_data["Close"]
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
st.write("이 데이터는 SPDR Gold Shares ETF (GLD)의 시세를 기반으로 합니다.")
