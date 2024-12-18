import streamlit as st
import plotly.graph_objects as go
import requests
import pandas as pd

# Alpha Vantage API 키 입력
ALPHA_VANTAGE_API_KEY = "44QLLQ0ELVP04SEY"

# 제목
st.title("실시간 금 시세 차트 및 테이블")
st.write("아래 메뉴를 사용해 일별, 월별, 연별 금 시세를 확인하세요.")

# 데이터 가져오기 함수
@st.cache_data
def get_real_gold_data():
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GLD&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" in data:
        # JSON 데이터 처리
        time_series = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        df = df.reset_index().rename(columns={"index": "Date"})
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")
        return df
    else:
        st.error("데이터를 불러오는 데 실패했습니다. API 키를 확인해주세요.")
        return pd.DataFrame()

# 데이터 가져오기
data = get_real_gold_data()

# 기간 선택 옵션
period = st.selectbox("원하는 기간을 선택하세요:", ["일별 시세", "월별 시세", "연별 시세"])

# 데이터 확인 및 차트 생성
if not data.empty:
    if period == "일별 시세":
        st.write("### 일별 시세 데이터")
        st.dataframe(data[["Date", "Close"]].head(10))  # 테이블 상단에 표시

        # 일별 차트
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data["Date"],
            y=data["Close"],
            mode="lines",
            fill="tonexty",
            line=dict(color="blue", width=2),
            name="Gold Price"
        ))
        fig.update_layout(title="일별 금 시세 차트", xaxis_title="날짜", yaxis_title="가격 (USD)")
        st.plotly_chart(fig)

    elif period == "월별 시세":
        # 월별 데이터 계산
        data["Year-Month"] = data["Date"].dt.to_period("M")
        monthly_data = data.groupby("Year-Month").agg({"Close": "mean"}).reset_index()
        monthly_data["Year-Month"] = monthly_data["Year-Month"].astype(str)

        st.write("### 월별 시세 데이터")
        st.dataframe(monthly_data)  # 테이블 상단에 표시

        # 월별 차트
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_data["Year-Month"],
            y=monthly_data["Close"],
            mode="lines+markers",
            line=dict(color="green", width=2),
            fill="tonexty",
            name="Monthly Avg Price"
        ))
        fig.update_layout(title="월별 금 시세 차트", xaxis_title="월", yaxis_title="평균 가격 (USD)")
        st.plotly_chart(fig)

    elif period == "연별 시세":
        # 연별 데이터 계산
        data["Year"] = data["Date"].dt.year
        yearly_data = data.groupby("Year").agg({"Close": "mean"}).reset_index()

        st.write("### 연별 시세 데이터")
        st.dataframe(yearly_data)  # 테이블 상단에 표시

        # 연별 차트
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=yearly_data["Year"],
            y=yearly_data["Close"],
            name="Yearly Avg Price"
        ))
        fig.update_layout(title="연별 금 시세 차트", xaxis_title="연도", yaxis_title="평균 가격 (USD)")
        st.plotly_chart(fig)
else:
    st.error("데이터를 가져오지 못했습니다. 다시 시도해주세요.")
