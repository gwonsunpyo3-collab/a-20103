import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("---")

# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre 열 전처리: 세로막대 기호(|)로 분리 후 첫 번째 장르만 추출
    df['genre'] = df['genre'].fillna('미상').astype(str).apply(lambda x: x.split('|')[0].strip())
    
    return df

df = load_data()

# -------------------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# Plotly 도넛 그래프 생성
fig_donut = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4,
    title="장르별 영화 비율 및 편수"
)

# 호버 툴팁 설정: 장르명, 편수(count), 비율(percent) 표시
fig_donut.update_traces(
    textposition='inside',
    textinfo='percent+label',
    hovertemplate="<b>장르:</b> %{label}<br><b>영화 편수:</b> %{value}편<br><b>비율:</b> %{percent}<extra></extra>"
)

fig_donut.update_layout(
    autosize=True,
    legend_title_text="장르"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_donut, use_container_width=True)

# 그래프 분석 내용 안내 구역
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info("여기에 분석 결과 한 문장을 입력하세요. (예: 드라마와 액션 장르가 전체 개봉 영화의 과반수 이상을 차지하며 높은 비중을 보입니다.)")

st.markdown("---")

# -------------------------------------------------------------------
# 두 번째 그래프: 장르 및 영화별 총 관객 수 (트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르 내 영화별 총 관객 수")

# 0이나 음수 등 비정상적인 관객 수 데이터 제외 (트리맵 에러 방지용)
df_treemap = df[df['total_audi'] > 0].copy()

# Plotly 트리맵 생성 (장르 안에 영화가 들어가도록 path 설정)
fig_treemap = px.treemap(
    df_treemap,
    path=['genre', 'movieNm'],
    values='total_audi',
    title="장르 및 영화별 관객 수 규모 (칸 크기 = 총 관객 수)"
)

# 호버 툴팁 설정: 영화명(또는 장르명)과 총 관객 수(천 단위 콤마 포함)
fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,.0f}명<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_treemap, use_container_width=True)

# 그래프 분석 내용 안내 구역
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info("여기에 분석 결과 한 문장을 입력하세요. (예: 액션 장르 내에서도 특정 몇몇 흥행작이 전체 관객 수의 대부분을 견인하고 있음을 확인할 수 있습니다.)")

st.markdown("---")
