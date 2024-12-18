import streamlit as st
import plotly.graph_objects as go
import requests
import pandas as pd

# Alpha Vantage API 키 입력
ALPHA_VANTAGE_API_KEY = "44QLLQ0ELVP04SEY"

# 데이터 가져오기 함수
@st.cache_data
def fetch_data():
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GLD&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" in data:
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        df.index = pd.to_datetime(df.index)
        df = df.reset_index().rename(columns={"index": "Date"})
        df = df.sort_values("Date", ascending=False)
        return df
    else:
        st.error("데이터를 불러오지 못했습니다. API 키를 확인해주세요.")
        return pd.DataFrame()

# 데이터 가져오기
data = fetch_data()

# 제목과 옵션 선택
st.title("실시간 금 시세 차트 및 도표")
period = st.selectbox("원하는 기간을 선택하세요:", ["일별 시세", "월별 시세", "연별 시세"])

# 데이터 확인
if not data.empty:
    if period == "일별 시세":
        st.write("### 일별 시세 도표")
        daily_data = data[["Date", "Close"]].head(7)  # 최근 7일 데이터
        st.dataframe(daily_data)

        st.write("### 일별 시세 차트")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_data["Date"],
            y=daily_data["Close"],
            mode="lines+markers",
            fill="tonexty",
            line=dict(color="blue", width=2),
            name="Daily Gold Price"
        ))
        fig.update_layout(title="일별 금 시세 차트", xaxis_title="날짜", yaxis_title="가격 (USD)")
        st.plotly_chart(fig)

    elif period == "월별 시세":
        st.write("### 월별 시세 도표")
        data["Year-Month"] = data["Date"].dt.to_period("M")
        monthly_data = data.groupby("Year-Month")["Close"].mean().reset_index()
        monthly_data["Year-Month"] = monthly_data["Year-Month"].astype(str)
        st.dataframe(monthly_data.head(5))  # 최근 5개월 데이터

        st.write("### 월별 시세 차트")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_data["Year-Month"],
            y=monthly_data["Close"],
            mode="lines+markers",
            fill="tonexty",
            line=dict(color="green", width=2),
            name="Monthly Gold Price"
        ))
        fig.update_layout(title="월별 금 시세 차트", xaxis_title="월", yaxis_title="평균 가격 (USD)")
        st.plotly_chart(fig)

    elif period == "연별 시세":
        st.write("### 연별 시세 도표")
        data["Year"] = data["Date"].dt.year
        yearly_data = data.groupby("Year")["Close"].mean().reset_index()
        st.dataframe(yearly_data)  # 연별 데이터 표시

        st.write("### 연별 시세 차트")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=yearly_data["Year"],
            y=yearly_data["Close"],
            name="Yearly Avg Gold Price"
        ))
        fig.update_layout(title="연별 금 시세 차트", xaxis_title="연도", yaxis_title="평균 가격 (USD)")
        st.plotly_chart(fig)
else:
    st.error("데이터를 불러올 수 없습니다. 다시 시도해주세요.")
