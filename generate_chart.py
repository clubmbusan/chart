import streamlit as st
import plotly.graph_objects as go
import requests
import pandas as pd

# Alpha Vantage API 키 입력
ALPHA_VANTAGE_API_KEY = "44QLLQ0ELVP04SEY"
SYMBOL = "GLD"  # 금 ETF 심볼 (Gold ETF)

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    # Alpha Vantage API 요청
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&outputsize=full&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # 데이터프레임 변환
    df = pd.DataFrame(data['Time Series (Daily)']).T
    df = df.rename(columns={'4. close': 'Close'})  # 종가 컬럼명 변경
    df.index = pd.to_datetime(df.index)  # 날짜 인덱스 설정
    df['Close'] = df['Close'].astype(float)
    return df[['Close']]

# 데이터 그룹화 함수
def group_data(df, period):
    if period == "daily":
        return df.reset_index().rename(columns={'index': 'Date'})
    elif period == "monthly":
        df['Year-Month'] = df.index.to_period('M')
        return df.groupby('Year-Month')['Close'].mean().reset_index()
    elif period == "yearly":
        df['Year'] = df.index.year
        return df.groupby('Year')['Close'].mean().reset_index()

# 데이터 로드
df = load_data()

# Streamlit 앱 제목 및 옵션
st.title("📈 실시간 금 시세 차트 및 도표")

# 기간 선택
option = st.selectbox("원하는 기간을 선택하세요:", ["일별 시세", "월별 시세", "연별 시세"])

# 선택된 옵션에 따라 데이터 표시
if option == "일별 시세":
    grouped_data = group_data(df, "daily")
    st.subheader("일별 시세 도표")
    st.dataframe(grouped_data.tail(10))  # 최근 10일 데이터 표시

    st.subheader("일별 금 시세 차트")
    fig = px.line(grouped_data, x="Date", y="Close", title="일별 금 시세 변화", markers=True)
    st.plotly_chart(fig)

elif option == "월별 시세":
    grouped_data = group_data(df, "monthly")
    st.subheader("월별 시세 도표")
    st.dataframe(grouped_data.tail(12))  # 최근 12개월 데이터 표시

    st.subheader("월별 금 시세 차트")
    fig = px.area(grouped_data, x="Year-Month", y="Close", title="월별 금 시세 변화", markers=True)
    st.plotly_chart(fig)

elif option == "연별 시세":
    grouped_data = group_data(df, "yearly")
    st.subheader("연별 시세 도표")
    st.dataframe(grouped_data)

    st.subheader("연별 금 시세 차트")
    fig = px.bar(grouped_data, x="Year", y="Close", title="연별 금 시세 변화", color="Close")
    st.plotly_chart(fig)

# API 출처 및 설명
st.caption("데이터 출처: Alpha Vantage API | 15분 지연 데이터")


