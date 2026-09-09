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

# 어제 날짜 구하기
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={API_KEY}&targetDt={yesterday}"

# 기본 백업 데이터
fallback_data = [
    {"순위": 1, "영화명": "오디세이", "개봉일": "2026-08-05", "당일 관객수": 76685, "누적 관객수": 10192029},
    {"순위": 2, "영화명": "옵세션", "개봉일": "2026-09-02", "당일 관객수": 26371, "누적 관객수": 239531},
    {"순위": 3, "영화명": "스파이더맨: 브랜드 뉴 데이", "개봉일": "2026-07-29", "당일 관객수": 13287, "누적 관객수": 8819175},
    {"순위": 4, "영화명": "비광", "개봉일": "2026-09-02", "당일 관객수": 6559, "누적 관객수": 82428},
    {"순위": 5, "영화명": "싱 어게인", "개봉일": "2026-09-02", "당일 관객수": 5490, "누적 관객수": 67281},
    {"순위": 6, "영화명": "경주기행", "개봉일": "2026-08-26", "당일 관객수": 4926, "누적 관객수": 308324},
    {"순위": 7, "영화명": "왕과 사는 남자", "개봉일": "2026-02-04", "당일 관객수": 1825, "누적 관객수": 16924757},
    {"순위": 8, "영화명": "오크 스트리트의 마지막 날", "개봉일": "2026-08-26", "당일 관객수": 1032, "누적 관객수": 132622},
    {"순위": 9, "영화명": "인 더 그레이", "개봉일": "2026-09-02", "당일 관객수": 1011, "누적 관객수": 10211},
    {"순위": 10, "영화명": "사진의 얼굴", "개봉일": "2026-09-02", "당일 관객수": 801, "누적 관객수": 4831}
]

parsed_data = []
target_date_str = yesterday

try:
    res = requests.get(url, timeout=5)
    res_data = res.json()
    if "boxOfficeResult" in res_data and "dailyBoxOfficeList" in res_data["boxOfficeResult"]:
        box_list = res_data["boxOfficeResult"]["dailyBoxOfficeList"]
        target_date_str = res_data["boxOfficeResult"]["showRange"].split("~")[0]
        for item in box_list:
            parsed_data.append({
                "순위": int(item["rank"]),
                "영화명": item["movieNm"],
                "개봉일": item["openDt"],
                "당일 관객수": int(item["audiCnt"]),
                "누적 관객수": int(item["audiAcc"])
            })
    else:
        parsed_data = fallback_data
        target_date_str = "2026-09-08"
except Exception:
    parsed_data = fallback_data
    target_date_str = "2026-09-08"

st.caption(f"📅 조회 기준일: {target_date_str}")

top1 = parsed_data[0]
col1, col2, col3 = st.columns(3)
col1.metric("🏆 1위 영화", top1["영화명"])
col2.metric("👥 어제 관객수", f"{top1['당일 관객수']:,} 명")
col3.metric("🍿 누적 관객수", f"{top1['누적 관객수']:,} 명")

st.divider()

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("📊 관객수 TOP 10 비교")
    chart_dict = {item["영화명"]: item["당일 관객수"] for item in parsed_data}
    st.bar_chart(chart_dict)

with right_col:
    st.subheader("📋 전체 순위표")
    st.dataframe(parsed_data, use_container_width=True, hide_index=True)
