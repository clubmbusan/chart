import plotly.express as px
import pandas as pd

# 예시 데이터
data = {
    "날짜": ["2024-12-01", "2024-12-05", "2024-12-10", "2024-12-15", "2024-12-20"],
    "1kg_가격(USD)": [7845, 7880, 7900, 7950, 8000],
}
df = pd.DataFrame(data)

# Plotly로 대화형 차트 생성
fig = px.line(df, x="날짜", y="1kg_가격(USD)", title="2024년 12월 1kg 금 가격 시세 변화")
fig.write_html("gold_price_chart.html")  # HTML 파일로 저장
