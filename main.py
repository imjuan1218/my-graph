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

st.divider()


# ----------------------------------------------------
# 구역 2: 일관객 합계 상위 5개 영화의 일관객 추이 비교
# ----------------------------------------------------
st.header("📌 구역 2: 관객수 TOP 5 영화의 일일 관객수 추이 비교")

# 1. 일관객 합계(총 관객수) 기준 상위 5개 영화 선정
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .nlargest(5)
    .index
    .tolist()
)

# 2. 상위 5개 영화 데이터만 필터링 및 날짜순 정렬
top5_df = df[df["영화명"].isin(top5_movies)].sort_values("날짜")

# 3. Plotly 다중 선 그래프 생성 (color='영화명'으로 영화별 색상 구분)
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    title="총 관객수 상위 5개 영화의 일일 관객수 변화 비교",
    labels={"날짜": "날짜", "일관객": "일일 관객수(명)", "영화명": "영화 제목"},
    markers=True,
)

# 마우스 호버(Hover) 시 세부 정보 포맷팅
fig2.update_traces(
    hovertemplate="<b>영화명</b>: %{fullData.name}<br><b>날짜</b>: %{x|%Y-%m-%d}<br><b>일일 관객수</b>: %{y:,}명<extra></extra>"
)

# 레이아웃 설정 (범례 클릭 시 켜고 끌 수 있음)
fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일일 관객수(명)",
    hovermode="x unified",
)

# 그래프 출력
st.plotly_chart(fig2, use_container_width=True)

# 4. 사용자가 직접 작성하는 '이 그래프로 알 수 있는 것' 영역
user_insight_2 = st.text_input(
    "📝 이 그래프로 알 수 있는 것 (직접 작성):",
    placeholder="예: 흥행 상위 영화들의 흥행 유지 기간과 피크 시점을 비교해볼 수 있다.",
    key="insight_top5",
)

if user_insight_2:
    st.info(f"💡 **이 그래프로 알 수 있는 것:** {user_insight_2}")
else:
    st.caption("위 입력 창에 그래프 분석 내용을 직접 입력해 보세요.")

# ----------------------------------------------------
# 구역 3: 날짜별 Top 10 관객수 합계 영역 그래프
# ----------------------------------------------------
st.header("📌 구역 3: 일별 박스오피스 TOP 10 총관객수 추이")

# 1. 날짜별 일관객 합계 계산
daily_total_df = (
    df.groupby("날짜", as_index=False)["일관객"].sum().sort_values("날짜")
)

# 2. Plotly 영역 그래프(Area Chart) 생성
fig3 = px.area(
    daily_total_df,
    x="날짜",
    y="일관객",
    title="일별 TOP 10 영화 관객수 합계 추이",
    labels={"날짜": "날짜", "일관객": "10위권 총관객수(명)"},
)

# 마우스 호버(Hover) 시 세부 정보 포맷팅
fig3.update_traces(
    hovertemplate="<b>날짜</b>: %{x|%Y-%m-%d}<br><b>TOP 10 총관객수</b>: %{y:,}명<extra></extra>"
)

# 3. 관객수 합계 상위 3일 구하기
top3_days = daily_total_df.nlargest(3, "일관객")

# 4. 그래프 위에 최상위 3일 날짜 및 관객수 텍스트 표기 (주석/Annotation)
for rank, (_, row) in enumerate(top3_days.iterrows(), start=1):
    date_str = row["날짜"].strftime("%Y-%m-%d")
    val_str = f"{row['일관객']:,}명"

    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=f"<b>🏆 {rank}위: {date_str}</b><br>({val_str})",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,  # 화살표 및 텍스트 위치를 점 상단으로 띄움
        font=dict(size=12, color="crimson"),
        bgcolor="white",
        bordercolor="crimson",
        borderwidth=1,
    )

# 레이아웃 설정
fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 총관객수(명)",
    hovermode="x unified",
)

# 그래프 출력
st.plotly_chart(fig3, use_container_width=True)

# 5. 사용자가 직접 작성하는 '이 그래프로 알 수 있는 것' 영역
user_insight_3 = st.text_input(
    "📝 이 그래프로 알 수 있는 것 (직접 작성):",
    placeholder="예: 극장가 전체의 성수기(명절, 연휴 등) 피크 시점과 전체 관객 규모를 파악할 수 있다.",
    key="insight_daily_total",
)

if user_insight_3:
    st.info(f"💡 **이 그래프로 알 수 있는 것:** {user_insight_3}")
else:
    st.caption("위 입력 창에 그래프 분석 내용을 직접 입력해 보세요.")


# ----------------------------------------------------
# 구역 4: 이 기간 일관객 합계 TOP 10 영화 (가로 막대그래프)
# ----------------------------------------------------
st.header("📌 구역 4: 기간 내 관객수 TOP 10 영화")

# 1. 영화별 총 관객수 합계 및 10위권 진입 일수(날수) 집계
top10_summary = (
    df.groupby("영화명")
    .agg(
        총관객수=("일관객", "sum"),
        진입일수=("날짜", "nunique"),  # 10위권에 든 일수
    )
    .reset_index()
)

# 2. 총관객수 기준 상위 10개 영화 추출 및 관객수 적은 순 정렬 (그래프 위쪽이 1위가 되도록)
top10_movies_df = top10_summary.nlargest(10, "총관객수").sort_values(
    "총관객수", ascending=True
)

# 3. Plotly 가로 막대그래프 생성
fig4 = px.bar(
    top10_movies_df,
    x="총관객수",
    y="영화명",
    orientation="h",
    title="기간 내 일관객 합계 TOP 10 영화",
    labels={
        "총관객수": "기간 내 총 관객수(명)",
        "영화명": "영화 제목",
        "진입일수": "10위권 진입 일수",
    },
    text_auto=",",  # 막대 끝에 관객수 표기 (천 단위 쉼표)
    hover_data={"진입일수": True},  # 마우스 호버 시 10위권 진입 일수 포함
)

# 마우스 호버(Hover) 시 세부 정보 포맷팅
fig4.update_traces(
    hovertemplate="<b>영화명</b>: %{y}<br><b>기간 내 총 관객수</b>: %{x:,}명<br><b>10위권 진입 일수</b>: %{customdata[0]}일<extra></extra>"
)

# 레이아웃 설정
fig4.update_layout(
    xaxis_title="기간 내 총 관객수(명)",
    yaxis_title="영화 제목",
    showlegend=False,
)

# 그래프 출력
st.plotly_chart(fig4, use_container_width=True)

# 4. 사용자가 직접 작성하는 '이 그래프로 알 수 있는 것' 영역
user_insight_4 = st.text_input(
    "📝 이 그래프로 알 수 있는 것 (직접 작성):",
    placeholder="예: 10위권에 장기 집권(진입 일수)한 영화일수록 총 관객수 합계가 높게 나타나는 경향이 있다.",
    key="insight_top10_bar",
)

if user_insight_4:
    st.info(f"💡 **이 그래프로 알 수 있는 것:** {user_insight_4}")
else:
    st.caption("위 입력 창에 그래프 분석 내용을 직접 입력해 보세요.")

# ----------------------------------------------------
# 구역 5: 월 × 요일별 일관객 합계 히트맵
# ----------------------------------------------------
st.header("📌 구역 5: 월 × 요일별 일관객 합계 분포 (히트맵)")

# 1. 월과 요일 추출
df_heatmap = df.copy()
df_heatmap["월"] = df_heatmap["날짜"].dt.month.map(lambda x: f"{x}월")
df_heatmap["요일"] = df_heatmap["날짜"].dt.day_name()

# 요일 한글 변환 매핑 및 월~일 순서 정의
day_map = {
    "Monday": "월요일",
    "Tuesday": "화요일",
    "Wednesday": "수요일",
    "Thursday": "목요일",
    "Friday": "금요일",
    "Saturday": "토요일",
    "Sunday": "일요일",
}
days_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일",
]
months_order = [f"{m}월" for m in range(1, 13)]

df_heatmap["요일"] = df_heatmap["요일"].map(day_map)

# 2. 월 × 요일 피벗 테이블 생성 (일관객 합계)
pivot_df = (
    df_heatmap.pivot_table(
        index="월", columns="요일", values="일관객", aggfunc="sum"
    )
    .reindex(index=months_order, columns=days_order)
    .fillna(0)
)

# 3. Plotly 히트맵 생성 (진할수록 관객이 많아지도록 Reds/Viridis 계열 색상 설정)
fig5 = px.imshow(
    pivot_df,
    labels=dict(x="요일", y="월", color="일관객 합계(명)"),
    x=days_order,
    y=months_order,
    color_continuous_scale="Reds",  # 색이 진할수록 관객 수가 많음
    title="월 × 요일별 일관객 합계 분포",
    text_auto=",.0f",  # 셀 안에 관객수 수치 표기 (천 단위 쉼표)
)

# 마우스 호버(Hover) 시 세부 정보 포맷팅
fig5.update_traces(
    hovertemplate="<b>%{y} %{x}</b><br><b>일관객 합계</b>: %{z:,}명<extra></extra>"
)

# 레이아웃 설정
fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
)

# 그래프 출력
st.plotly_chart(fig5, use_container_width=True)

# 4. 사용자가 직접 작성하는 '이 그래프로 알 수 있는 것' 영역
user_insight_5 = st.text_input(
    "📝 이 그래프로 알 수 있는 것 (직접 작성):",
    placeholder="예: 연휴 및 성수기 시즌의 특정 요일(주말 등)에 관객 집중도가 극대화되는 것을 볼 수 있다.",
    key="insight_heatmap",
)

if user_insight_5:
    st.info(f"💡 **이 그래프로 알 수 있는 것:** {user_insight_5}")
else:
    st.caption("위 입력 창에 그래프 분석 내용을 직접 입력해 보세요.")
