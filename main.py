import pandas as pd
import plotly.graph_objects as go
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
# 누적관객수(최댓값) 기준으로 영화명을 내림차순 정렬하여 중복 없이 추출
movie_rank = (
    df.groupby("영화명")["누적관객수"]
    .max()
    .reset_index()
    .sort_values(by="누적관객수", ascending=False)
)
movie_list = movie_rank["영화명"].tolist()

# TOP 10 차트 등장 일수가 20일 이상인 영화 중 누적관객수 상위 5개 추출
movie_days = df.groupby("영화명")["기준일자"].count()
over_20days_movies = movie_days[movie_days >= 20].index
filtered_movie_rank = movie_rank[movie_rank["영화명"].isin(over_20days_movies)]
top5_movies = filtered_movie_rank.head(5)["영화명"].tolist()

# 사이드바에서 영화 선택
st.sidebar.header("📌 설정")
selected_movie = st.sidebar.selectbox("분석할 영화를 선택하세요", movie_list)

# 선택한 영화의 데이터만 필터링
filtered_df = df[df["영화명"] == selected_movie]

# 메인 화면 레이아웃 구역 나누기 (Tab 활용)
tab1, tab2, tab3, tab4 = st.tabs([
    "일별 관객수 추이 (선 그래프)",
    "누적 관객수 변화 (영역 차트)",
    "TOP 5 영화 비교 (20일 이상 차트인)",
    "전체 관객수 7일 이동평균 (선 그래프)",
])

# [4. 첫 번째 그래프: 선그래프]
with tab1:
    st.subheader(f"📊 '{selected_movie}' 일별 관객수 변화")

    fig_line = px.line(
        filtered_df,
        x="기준일자",
        y="해당일관객수",
        title=f"{selected_movie} - 일별 관객수 추이",
        labels={"기준일자": "날짜", "해당일관객수": "일별 관객수(명)"},
        markers=True,
    )
    fig_line.update_layout(hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)

    st.info(
        f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}의 개봉 초기 관객 집중도 및 상영 기간 동안의 일자별 흥행 추이를 한눈에 확인할 수 있습니다."
    )

# [5. 두 번째 그래프: 영역차트]
with tab2:
    st.subheader(f"📈 '{selected_movie}' 누적 관객수 변화")

    fig_area = px.area(
        filtered_df,
        x="기준일자",
        y="누적관객수",
        title=f"{selected_movie} - 누적 관객수 증가 추이",
        labels={"기준일자": "날짜", "누적관객수": "누적 관객수(명)"},
    )
    fig_area.update_layout(hovermode="x unified")
    st.plotly_chart(fig_area, use_container_width=True)

    st.info(
        f"💡 **이 그래프로 알 수 있는 것:** 상영 기간 동안 {selected_movie}의 누적 관객수가 완만하게 또는 가파르게 증가하는지 볼 수 있으며, 최종 누적 관객수에 도달하는 속도를 파악할 수 있습니다."
    )

# [6. 세 번째 그래프: 다중 선그래프 (20일 이상 차트인 & TOP 5 비교)]
with tab3:
    st.subheader("🏆 TOP 10에 20일 이상 유지된 누적 관객수 상위 5개 영화 비교")

    top5_df = df[df["영화명"].isin(top5_movies)]

    fig_top5 = px.line(
        top5_df,
        x="기준일자",
        y="누적관객수",
        color="영화명",
        title="장기 흥행 영화(20일 이상 TOP 10 유지) 상위 5개의 누적 관객수 추이 비교",
        labels={"기준일자": "날짜", "누적관객수": "누적 관객수(명)", "영화명": "영화 제목"},
    )
    fig_top5.update_layout(hovermode="x unified")
    st.plotly_chart(fig_top5, use_container_width=True)

    top5_names_str = ", ".join(top5_movies)
    st.info(
        f"💡 **이 그래프로 알 수 있는 것:** TOP 10 박스오피스에 최소 20일 이상 머무르며 장기 흥행에 성공한 대표적인 5개 영화({top5_names_str})의 누적 관객수 증가 양상을 비교 분석할 수 있습니다."
    )

# [7. 네 번째 그래프: 전체 관객수 합계 및 7일 이동평균]
with tab4:
    st.subheader("📉 기준일자별 TOP10 전체 관객수 및 7일 이동평균")

    # 기준일자별로 모든 TOP10 영화의 해당일관객수 합계 계산
    daily_total = (
        df.groupby("기준일자")["해당일관객수"].sum().reset_index()
    )

    # 7일 이동평균선 계산
    daily_total["7일이동평균"] = (
        daily_total["해당일관객수"].rolling(window=7).mean()
    )

    # graph_objects를 사용하여 두 선의 스타일(연하게/진하게)을 커스텀 정의
    fig_ma = go.Figure()

    # 원본 관객수 합계 선 (연한 색상)
    fig_ma.add_trace(
        go.Scatter(
            x=daily_total["기준일자"],
            y=daily_total["해당일관객수"],
            mode="lines",
            name="일별 관객수 합계",
            line=dict(color="rgba(100, 149, 237, 0.35)", width=1.5),
        )
    )

    # 7일 이동평균 선 (진한 색상)
    fig_ma.add_trace(
        go.Scatter(
            x=daily_total["기준일자"],
            y=daily_total["7일이동평균"],
            mode="lines",
            name="7일 이동평균",
            line=dict(color="#1f77b4", width=3),
        )
    )

    # 레이아웃 설정
    fig_ma.update_layout(
        title="전체 박스오피스 일별 관객수 합계 및 7일 이동평균 추이",
        xaxis_title="날짜",
        yaxis_title="관객수(명)",
        hovermode="x unified",
    )

    st.plotly_chart(fig_ma, use_container_width=True)

    st.info(
        "💡 **이 그래프로 알 수 있는 것:** 요일별 단기 변동(주말 급증 등)에 따른 노이즈를 줄이고, 전체 극장가의 성수기/비성수기 등 전반적인 시장 흐름과 관객수 변화 추세를 명확하게 확인할 수 있습니다."
    )
