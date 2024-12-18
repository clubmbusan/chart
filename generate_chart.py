import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 제목 설정
st.title("2024년 12월 금 시세 변화")
st.write("이 페이지에서는 금 1kg의 시세 변화를 확인할 수 있습니다.")

# 데이터 준비
data = {
    "날짜": pd.date_range(start="2024-12-01", end="2024-12-20"),
    "가격": [7850 + i * 50 for i in range(20)]
}
df = pd.DataFrame(data)

# Plotly 차트 생성
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["날짜"], y=df["가격"], mode="lines+markers", name="금 시세"))
fig.update_layout(title="1kg 금 시세 변화", xaxis_title="날짜", yaxis_title="가격 (USD)")

# 차트 출력
st.plotly_chart(fig)

# 추가 메시지
st.write("위 차트는 2024년 12월 금 시세 변화를 보여줍니다.")
