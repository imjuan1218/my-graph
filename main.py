import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption("1년치 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 변화를 시각화합니다.")


# ----------------------------------------------------
# 1. 데이터 불러오기 및 전처리 (캐싱 적용)
# ----------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)

    # '날짜' 열을 문자열로 다룬 뒤 실제 datetime 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")

    # 숫자형 컬럼 변환 (혹시 모를 문자열 형태 대비)
    numeric_cols = ["순위", "일관객", "누적관객", "스크린수", "상영횟수"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()

st.divider()

# ----------------------------------------------------
# 구역 1: 영화별 일일 관객수 추이 (시간의 흐름)
# ----------------------------------------------------
st.header("📌 구역 1: 영화별 일일 관객수 변화 추이")

# 드롭다운으로 영화 선택 (전체 영화 목록을 알파벳/가나다 순 정렬)
movie_list = sorted(df["영화명"].dropna().unique())
selected_movie = st.selectbox(
    "관객수 추이를 확인할 영화를 선택하세요:",
    movie_list,
    index=0 if movie_list else None,
)

if selected_movie:
    # 선택된 영화의 데이터 필터링 및 날짜순 정렬
    movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

    # Plotly 선 그래프 생성
    fig = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        title=f"'{selected_movie}'의 일일 관객수 변화",
        labels={"날짜": "날짜", "일관객": "일일 관객수(명)"},
        markers=True,  # 각 데이터 지점에 점 표시
    )

    # 마우스 호버(Hover) 시 날짜와 관객수가 포맷팅되어 보이도록 설정
    fig.update_traces(
        hovertemplate="<b>날짜</b>: %{x|%Y-%m-%d}<br><b>일일 관객수</b>: %{y:,}명<extra></extra>"
    )

    # 그래프 레이아웃 다듬기
    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="일일 관객수(명)",
        hovermode="x unified",
    )

    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 그래프 하단 인사이트 및 결론 문구 자리
    st.info(
        f"💡 **이 그래프로 알 수 있는 것:** "
        f"'{selected_movie}'은(는) 상영 기간 동안 최고 일일 관객수 **{movie_df['일관객'].max():,}명**을 기록하였으며, "
        f"시간이 지남에 따라 관객수가 어떻게 변화하고 추세가 꺾이는지 한눈에 파악할 수 있습니다."
    )

st.divider()

# ----------------------------------------------------
# 구역 2: 향후 새로운 시간 관련 그래프 추가 영역
# ----------------------------------------------------
st.header("📌 구역 2: (추가 예정 구역)")
st.caption("이곳에는 월별/요일별 박스오피스 종합 추이 등 새로운 시간 축 그래프가 추가될 예정입니다.")
# ----------------------------------------------------
# 구역 2: 향후 새로운 시간 관련 그래프 추가 및 분석 영역
# ----------------------------------------------------
st.header("📌 구역 2: (추가 예정 구역)")

# 사용자가 직접 문구를 작성하여 메모할 수 있는 공간
user_insight_2 = st.text_input(
    "📝 이 그래프로 알 수 있는 것 (직접 작성):",
    placeholder="구역 2 그래프 분석 내용을 작성하세요.",
    key="insight_zone_2",
)

if user_insight_2:
    st.info(f"💡 **이 그래프로 알 수 있는 것:** {user_insight_2}")
else:
    st.caption("위 입력 창에 그래프 분석 내용을 직접 입력해 보세요.")
