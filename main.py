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
    df['nation'] = df['nation'].fillna('기타').astype(str).apply(lambda x: x.strip())
    
    return df

df = load_data()

# -------------------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig_donut = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4,
    title="장르별 영화 비율 및 편수"
)

fig_donut.update_traces(
    textposition='inside',
    textinfo='percent+label',
    hovertemplate="<b>장르:</b> %{label}<br><b>영화 편수:</b> %{value}편<br><b>비율:</b> %{percent}<extra></extra>"
)

fig_donut.update_layout(autosize=True, legend_title_text="장르")
st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info("드라마와 액션 장르가 전체 개봉 영화의 과반수 이상을 차지하며 높은 비중을 보입니다.")

st.markdown("---")

# -------------------------------------------------------------------
# 두 번째 그래프: 장르 및 영화별 총 관객 수 (트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르 내 영화별 총 관객 수")

df_treemap = df[df['total_audi'] > 0].copy()

fig_treemap = px.treemap(
    df_treemap,
    path=['genre', 'movieNm'],
    values='total_audi',
    title="장르 및 영화별 관객 수 규모 (칸 크기 = 총 관객 수)"
)

fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info("액션 장르 내에서도 특정 몇몇 흥행작이 전체 관객 수의 대부분을 견인하고 있음을 확인할 수 있습니다.")

st.markdown("---")

# -------------------------------------------------------------------
# 세 번째 그래프: 총 관객 수 분포 (히스토그램)
# -------------------------------------------------------------------
st.subheader("3. 총 관객 수 분포")

fig_hist = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="영화별 총 관객 수 분포",
    labels={'total_audi': '총 관객 수 (명)', 'count': '영화 수'}
)

fig_hist.update_traces(
    hovertemplate="<b>관객 수 구간:</b> %{x}<br><b>영화 수:</b> %{y}편<extra></extra>"
)

fig_hist.update_layout(
    xaxis_title="총 관객 수 (명)",
    yaxis_title="영화 수 (편)",
    bargap=0.1
)

st.plotly_chart(fig_hist, use_container_width=True)

top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info(
    f"대부분의 영화는 관객 수 최하위 구간(약 100만 명 이하)에 쏠려 있으며, "
    f"가장 많은 관객을 동원한 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,.0f}명)입니다."
)

st.markdown("---")

# -------------------------------------------------------------------
# 네 번째 그래프: 개봉일 스크린수 vs 총 관객 수 (산점도)
# -------------------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객 수의 관계")

fig_scatter = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 대비 총 관객 수 관계",
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객 수 (명)',
        'genre': '장르'
    }
)

fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수 (개)",
    yaxis_title="총 관객 수 (명)"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info("개봉일 스크린수가 확보될수록 대체로 총 관객 수가 증가하는 경향을 보이지만, 초기 스크린수가 적더라도 입소문 등을 통해 대형 흥행을 이뤄낸 이상치(Outlier) 영화도 존재합니다.")

st.markdown("---")

# -------------------------------------------------------------------
# 다섯 번째 그래프: 10편 이상 장르별 총 관객 수 박스플롯
# -------------------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객 수 (박스플롯)")

top_genres = df['genre'].value_counts()[lambda x: x >= 10].index
df_filtered_box = df[df['genre'].isin(top_genres)].copy()

fig_box = px.box(
    df_filtered_box,
    x='genre',
    y='total_audi',
    color='genre',
    hover_data={'movieNm': True, 'total_audi': ':,', 'genre': False},
    points='outliers',
    title="영화 수 10편 이상 장르의 총 관객 수 분포",
    labels={
        'genre': '장르',
        'total_audi': '총 관객 수 (명)',
        'movieNm': '영화명'
    }
)

fig_box.update_traces(
    hovertemplate="<b>영화명:</b> %{customdata[0]}<br><b>총 관객 수:</b> %{y:,.0f}명<extra></extra>"
)

fig_box.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객 수 (명)",
    showlegend=False
)

st.plotly_chart(fig_box, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info("대부분 장르의 중위 관객 수 분포는 낮게 형성되어 있으나, 상단 이상치(Outlier)로 튀는 대형 흥행작들에 의해 평균과 최대 관객 수의 격차가 매우 커집니다.")

st.markdown("---")

# -------------------------------------------------------------------
# 여섯 번째 그래프: 개봉일 스크린수 vs 총 관객 수 버블 그래프
# -------------------------------------------------------------------
st.subheader("6. 개봉일 스크린수와 총 관객 수의 관계 (버블 크기: 개봉 첫 주 관객)")

fig_bubble = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    size_max=50,
    title="개봉일 스크린수 vs 총 관객 수 (버블 크기 = 개봉 첫 주 관객)",
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객 수 (명)',
        'first_week_audi': '개봉 첫 주 관객 (명)',
        'genre': '장르'
    }
)

fig_bubble.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<br>첫 주 관객 수: %{marker.size:,.0f}명<extra></extra>"
)

fig_bubble.update_layout(
    xaxis_title="개봉일 스크린수 (개)",
    yaxis_title="총 관객 수 (명)"
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info("개봉 첫 주 관객(버블 크기)이 많을수록 최종 총 관객 수도 크게 증가하는 강력한 정적 상관관계를 확인할 수 있습니다.")

st.markdown("---")

# -------------------------------------------------------------------
# 일곱 번째 그래프: 제작 국가별 장르 분포 (선버스트 그래프)
# -------------------------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 (선버스트 그래프)")

df_sunburst = df.groupby(['nation', 'genre']).size().reset_index(name='movie_count')

fig_sunburst = px.sunburst(
    df_sunburst,
    path=['nation', 'genre'],
    values='movie_count',
    title="제작 국가 → 장르 계층구조별 영화 편수 (칸 크기 = 영화 편수)"
)

fig_sunburst.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig_sunburst, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info("한국과 미국 등 주요 제작 국가에 따라 주로 제작 및 개봉되는 중심 장르의 구성 비중에 확연한 차이가 나타납니다.")

st.markdown("---")

# -------------------------------------------------------------------
# 여덟 번째 그래프: 질문 기반 산점도
# -------------------------------------------------------------------
st.subheader("8. 개봉 첫주의 관객이 영화의 흥행에 어떤 영향을 주는가")

fig_q8 = px.scatter(
    df,
    x='days_in_top10',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    size_max=40,
    title="개봉 첫주의 관객이 영화의 흥행에 어떤 영향을 주는가",
    labels={
        'days_in_top10': '10위권에 머문 날수 (일)',
        'total_audi': '총 관객 수 (명)',
        'first_week_audi': '개봉 첫 주 관객 (명)',
        'genre': '장르'
    }
)

fig_q8.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>10위권 머문 날수: %{x}일<br>총 관객 수: %{y:,.0f}명<br>첫 주 관객 수: %{marker.size:,.0f}명<extra></extra>"
)

fig_q8.update_layout(
    xaxis_title="10위권에 머문 날수 (일)",
    yaxis_title="총 관객 수 (명)"
)

st.plotly_chart(fig_q8, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.info("개봉 첫 주 관객 수(점의 크기)가 많은 영화일수록 10위권에 오래 장기 집권(X축)하며 최종 총 관객 수(Y축)도 압도적으로 높아져 초기 흥행이 장기 흥행으로 연결됨을 알 수 있습니다.")

st.markdown("---")
