import streamlit as st
st.title("나의 데이터 과학 포트폴리오")
st.write("반갑습니다! 이제부터 여기에 제 작업을 기록합니다.")
st.write("권순표")
import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="일별 박스오피스 대시보드", page_icon="🎬", layout="wide")
st.title("🎬 일별 박스오피스 대시보드")

API_KEY = "0fc4b6c5695f840b08eba74b3dc3d3d2"

# 집계 가능한 가장 최근 날짜 (어제)
yesterday = datetime.now().date() - timedelta(days=1)

# 달력으로 날짜 선택 (최대 어제까지 선택 가능)
selected_date = st.date_input(
    "📅 조회할 날짜를 선택하세요",
    value=yesterday,
    max_value=yesterday
)

# API 요청용 YYYYMMDD 날짜 문자열
target_dt = selected_date.strftime("%Y%m%d")
url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={API_KEY}&targetDt={target_dt}"

parsed_data = []
is_empty = False

try:
    res = requests.get(url, timeout=5)
    res_data = res.json()
    
    if "boxOfficeResult" in res_data and "dailyBoxOfficeList" in res_data["boxOfficeResult"]:
        box_list = res_data["boxOfficeResult"]["dailyBoxOfficeList"]
        
        if not box_list:
            is_empty = True
        else:
            for item in box_list:
                rank_inten = int(item.get("rankInten", 0))
                
                # 순위 증감 표시 (양수: 빨간 위 화살표, 음수: 파란 아래 화살표)
                if rank_inten > 0:
                    change_str = f"🔴 ⬆️ {rank_inten}"
                elif rank_inten < 0:
                    change_str = f"🔵 ⬇️ {abs(rank_inten)}"
                else:
                    change_str = "➖ 0"
                
                # 누적 관객수 100만 명 이상 트로피 표시
                audi_acc = int(item.get("audiAcc", 0))
                movie_name = item.get("movieNm", "")
                if audi_acc >= 1000000:
                    movie_name = f"{movie_name} 🏆"
                
                parsed_data.append({
                    "순위": int(item.get("rank", 0)),
                    "순위 변동": change_str,
                    "영화명": movie_name,
                    "개봉일": item.get("openDt", "-"),
                    "당일 관객수": int(item.get("audiCnt", 0)),
                    "누적 관객수": audi_acc
                })
    else:
        is_empty = True

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    is_empty = True

# 결과 출력
if is_empty or not parsed_data:
    st.warning("그날은 아직 집계 전입니다")
else:
    # 요약 지표
    top1 = parsed_data[0]
    col1, col2, col3 = st.columns(3)
    col1.metric("🏆 1위 영화", top1["영화명"])
    col2.metric("👥 당일 관객수", f"{top1['당일 관객수']:,} 명")
    col3.metric("🍿 누적 관객수", f"{top1['누적 관객수']:,} 명")

    st.divider()

    # 차트 및 표
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("📊 관객수 TOP 10 비교")
        chart_dict = {item["영화명"]: item["당일 관객수"] for item in parsed_data}
        st.bar_chart(chart_dict)

    with right_col:
        st.subheader("📋 전체 순위표")
        st.dataframe(parsed_data, use_container_width=True, hide_index=True)
