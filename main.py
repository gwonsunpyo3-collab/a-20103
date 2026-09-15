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

# 호버 툴팁 설정
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
st.info("드라마와 액션 장르가 전체 개봉 영화의 과반수 이상을 차지하며 높은 비중을 보입니다.")

st.markdown("---")

# -------------------------------------------------------------------
# 두 번째 그래프: 장르 및 영화별 총 관객 수 (트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르 내 영화별 총 관객 수")

# 0 이하 관객 수 데이터 제외
df_treemap = df[df['total_audi'] > 0].copy()

# Plotly 트리맵 생성
fig_treemap = px.treemap(
    df_treemap,
    path=['genre', 'movieNm'],
    values='total_audi',
    title="장르 및 영화별 관객 수 규모 (칸 크기 = 총 관객 수)"
)

# 호버 툴팁 설정
fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,.0f}명<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_treemap, use_container_width=True)

# 그래프 분석 내용 안내 구역
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info("액션 장르 내에서도 특정 몇몇 흥행작이 전체 관객 수의 대부분을 견인하고 있음을 확인할 수 있습니다.")

st.markdown("---")

# -------------------------------------------------------------------
# 세 번째 그래프: 총 관객 수 분포 (히스토그램)
# -------------------------------------------------------------------
st.subheader("3. 총 관객 수 분포")

# Plotly 히스토그램 생성
fig_hist = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="영화별 총 관객 수 분포",
    labels={'total_audi': '총 관객 수 (명)', 'count': '영화 수'}
)

# 호버 툴팁 설정
fig_hist.update_traces(
    hovertemplate="<b>관객 수 구간:</b> %{x}<br><b>영화 수:</b> %{y}편<extra></extra>"
)

fig_hist.update_layout(
    xaxis_title="총 관객 수 (명)",
    yaxis_title="영화 수 (편)",
    bargap=0.1
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_hist, use_container_width=True)

# 가장 관객 수가 많은 영화 정보 동적 추출
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# 그래프 분석 내용 안내 구역 (동적 분석 문구)
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info(
    f"대부분의 영화는 관객 수 최하위 구간(약 100만 명 이하)에 쏠려 있으며, "
    f"가장 많은 관객을 동원한 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,.0f}명)입니다."
)

st.markdown("---")
