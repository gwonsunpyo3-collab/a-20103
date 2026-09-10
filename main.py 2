import pandas as pd
import plotly.express as px
import streamlit as st

# [1. 데이터 불러오기 및 캐싱]
# @st.cache_data를 사용하여 데이터 불러오기 결과를 저장해두고 재사용합니다.
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/keep-growing-park/data-science/refs/heads/main/dataset/kobis_1year_boxoffice.csv"
    df = pd.read_csv(url)

    # [2. 데이터 전처리]
    # 결측치(NaN)가 포함된 행 삭제
    df = df.dropna()

    # '기준일자' 컬럼을 datetime 형식으로 변환
    df["기준일자"] = pd.to_datetime(df["기준일자"])

    # 기준일자 기준으로 오름차순 정렬
    df = df.sort_values(by="기준일자")

    return df


# 페이지 기본 설정
st.set_page_config(page_title="영화 박스오피스 분석 앱", layout="wide")
st.title("🎬 영화 박스오피스 데이터 분석")

# 데이터 로드
df = load_data()

# [3. 영화 선택 기능]
# 누적관객수(최댓값) 기준으로 영화명을 내림차순 정렬하여 중복 없이 extraction
movie_rank = (
    df.groupby("영화명")["누적관객수"]
    .max()
    .reset_index()
    .sort_values(by="누적관객수", ascending=False)
)
movie_list = movie_rank["영화명"].tolist()

# 사이드바에서 영화 선택
st.sidebar.header("📌 설정")
selected_movie = st.sidebar.selectbox("분석할 영화를 선택하세요", movie_list)

# 선택한 영화의 데이터만 필터링
filtered_df = df[df["영화명"] == selected_movie]

# 메인 화면 레이아웃 구역 나누기 (Tab 활용)
tab1, tab2 = st.tabs(["일별 관객수 추이", "추가 분석 구역 (예정)"])

# [4. 선그래프 그리기]
with tab1:
    st.subheader(f"📊 '{selected_movie}' 일별 관객수 변화")

    # Plotly 선 그래프 생성
    fig = px.line(
        filtered_df,
        x="기준일자",
        y="해당일관객수",
        title=f"{selected_movie} - 일별 관객수 추이",
        labels={"기준일자": "날짜", "해당일관객수": "일별 관객수(명)"},
        markers=True,  # 데이터 지점에 점 표시
    )

    # 그래프 레이아웃 커스텀
    fig.update_layout(hovermode="x unified")

    # Streamlit에 Plotly 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # [5. 그래프 설명 문구 자리]
    st.info(
        f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}의 개봉 초기 관객 집중도 및 상영 기간 동안의 흥행 추이를 한눈에 확인할 수 있습니다."
    )

# [5. 향후 그래프 추가를 위한 예시 구역]
with tab2:
    st.subheader("🚀 추후 새로운 분석 그래프가 추가될 공간입니다.")
    st.write("예: 주말 vs 평일 관객수 비교, 스크린수 대비 관객수 변화 등")

    # 향후 추가될 그래프 하단 설명 위치 예시
    st.info("💡 **이 그래프로 알 수 있는 것:** (추가 예정)")
