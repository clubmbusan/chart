import plotly.graph_objects as go
import pandas as pd

# 예제 데이터: 날짜별 금 시세
data = {
    "날짜": pd.date_range(start="2024-12-01", end="2024-12-20", freq="D"),
    "가격": [7850 + (i * 50) for i in range(20)]  # 단순 상승 시뮬레이션
}

# 데이터프레임 생성
df = pd.DataFrame(data)

# Plotly 그래프 객체 생성 (면적 차트로 변경)
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["날짜"],
    y=df["가격"],
    mode='lines',
    fill='tozeroy',  # 아래 면적 채우기
    line=dict(color='blue', width=2),
    name="1kg 금 시세"
))

# 레이아웃 설정: 인터랙티브 기능 추가
fig.update_layout(
    title="2024년 12월 1kg 금 가격 시세 변화",
    xaxis=dict(
        title="날짜",
        rangeslider=dict(visible=True),  # 날짜 슬라이더 추가
        type="date"  # X축을 날짜 형식으로 설정
    ),
    yaxis=dict(title="가격 (USD)"),
    template="plotly_white"  # 차트 배경 테마 설정
)

# HTML 파일로 저장
fig.write_html("index.html")
