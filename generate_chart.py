import plotly.graph_objects as go
import pandas as pd

# 예시 데이터: 날짜별 금 시세 시뮬레이션
data = {
    "날짜": pd.date_range(start="2024-12-01", end="2024-12-20", freq="D"),
    "가격": [243.5 + i*0.3 for i in range(20)]  # 단순한 가격 상승 데이터 예시
}

# 데이터프레임 생성
df = pd.DataFrame(data)

# Plotly 그래프 객체로 면적 차트 생성
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["날짜"],
    y=df["가격"],
    fill='tozeroy',  # 면적 채우기
    mode='lines',
    line=dict(color='red'),
    name="금 시세 (USD)"
))

# 차트 레이아웃 설정
fig.update_layout(
    title="2024년 12월 금 시세 인터랙티브 차트",
    xaxis_title="날짜",
    yaxis_title="가격 (USD)",
    xaxis=dict(
        rangeslider=dict(visible=True),  # 날짜 슬라이더 추가
        type="date"  # x축을 날짜 형식으로 설정
    ),
    template="plotly_white"
)

# HTML 파일로 저장
fig.write_html("index.html")
