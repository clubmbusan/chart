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

# 데이터가 비어있지 않으면 실행
if not data.empty:
    # 기간 선택 메뉴
    option = st.selectbox("원하는 기간을 선택하세요:", ["일별 시세", "월별 시세", "연별 시세"])

    # 날짜 기반 컬럼 추가
    data["월"] = data["Date"].dt.to_period("M").dt.to_timestamp()
    data["연"] = data["Date"].dt.to_period("Y").dt.to_timestamp()

    # 옵션별 데이터 처리
    if option == "일별 시세":
        filtered_data = data
        x_axis = filtered_data["Date"]
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

    # 선형 면적 차트 생성
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_axis, 
        y=y_axis, 
        mode="lines",  # 선형 그래프
        fill="tonexty",  # 면적 채우기 옵션
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

    # 데이터 테이블 표시
    st.write("### 데이터 테이블")
    st.dataframe(filtered_data)

    # 출처 표시
    st.write("이 데이터는 Alpha Vantage API를 통해 가져온 실시간 금 시세입니다.")

else:
    st.error("데이터를 가져오지 못했습니다. 다시 시도해주세요.")
