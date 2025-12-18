import streamlit as st
import os
import time

# ===== 세션 상태 =====
if "start" not in st.session_state:
    st.session_state.start = False
if "loading" not in st.session_state:
    st.session_state.loading = False

# ===== 스타일 =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
    background-color: #F5F5F5;
    color: #000000;
}

h1, h2 {
    text-align: center;
    font-weight: 700;
}

p {
    text-align: center;
    color: #333333;
}

.stButton>button {
    background: linear-gradient(90deg, #E0E0E0, #CCCCCC);
    color: #000000;
    font-weight: 700;
    font-size: 18px;
    height: 50px;
    width: 240px;
    border-radius: 15px;
    margin: auto;
    display: block;
    box-shadow: 0 6px 15px rgba(0,0,0,0.2);
    transition: transform 0.2s, background 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #CCCCCC, #AAAAAA);
}

.card {
    background: rgba(255, 255, 255, 0.95);
    padding: 20px;
    margin: 15px 0;
    border-radius: 20px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}

.card h3 {
    margin: 0;
    color: #000000;
    font-weight: 700;
}

.card p {
    margin: 5px 0;
    color: #000000;
}

a {
    color: #FF4081;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}

.footer {
    text-align: center;
    color: #666666;
    font-size: 14px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===== 인트로 화면 =====
if not st.session_state.start and not st.session_state.loading:
    st.markdown("<h1>cos</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:18px;'>최적의 화장품을, 최적의 가격으로.</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:14px; color:#666;'>여러 쇼핑몰의 가격 정보를 한눈에 확인하고, 스마트한 쇼핑을 경험하세요.</p>",
        unsafe_allow_html=True
    )

    if os.path.exists("cover.png"):
        st.image("cover.png", use_container_width=True)
    if os.path.exists("intro_animation.gif"):
        st.image("intro_animation.gif", width=300)

    if st.button("🚀 앱 시작하기"):
        st.session_state.loading = True
        st.rerun()

    st.markdown("<div class='footer'>아래로 스크롤하면 가격 비교 앱을 시작할 수 있어요</div>", unsafe_allow_html=True)

# ===== 로딩 화면 =====
elif st.session_state.loading and not st.session_state.start:
    st.markdown("<h2>⏳ 앱 로딩 중...</h2>", unsafe_allow_html=True)
    if os.path.exists("loading.gif"):
        st.image("loading.gif", width=250)
    else:
        with st.spinner("불러오는 중..."):
            time.sleep(2)
    progress = st.progress(0)
    for i in range(1, 101):
        time.sleep(0.01)
        progress.progress(i)
    st.session_state.start = True
    st.session_state.loading = False
    st.rerun()

# ===== 본 앱 화면 =====
else:
    st.title("cos")

    products = [
        # 쿠션
        {"name": "바닐라코 쿠션", "category": "쿠션", "prices": {
            "무신사": (22500, "https://www.musinsa.com/products/3539837"),
            "에이블리": (24500, "https://m.a-bly.com/goods/10764759"),
            "지그재그": (31920, "https://zigzag.kr/catalog/products/128826773")
        }},
        {"name": "페리페라 쿠션", "category": "쿠션", "prices": {
            "무신사": (18750, "https://www.musinsa.com/products/3304473"),
            "에이블리": (17000, "https://m.a-bly.com/goods/7268291"),
            "지그재그": (0, "#")  # 검색 결과 없음
        }},
        {"name": "클리오 쿠션", "category": "쿠션", "prices": {
            "무신사": (32400, "https://www.musinsa.com/products/5395290"),
            "에이블리": (24500, "https://m.a-bly.com/goods/52888117"),
            "지그재그": (28800, "https://zigzag.kr/catalog/products/165706125")
        }},
        # 팔레트
        {"name": "바닐라코 팔레트", "category": "팔레트", "prices": {
            "무신사": (11200, "https://www.musinsa.com/products/2534210"),
            "에이블리": (9000, "https://m.a-bly.com/goods/4197549"),
            "지그재그": (13000, "https://zigzag.kr/catalog/products/112135833")
        }},
        {"name": "클리오 팔레트", "category": "팔레트", "prices": {
            "무신사": (20930, "https://www.musinsa.com/products/4543710"),
            "에이블리": (26500, "https://www.musinsa.com/products/4543710"),
            "지그재그": (31900, "https://zigzag.kr/catalog/products/127248473")
        }},
        {"name": "페리페라 팔레트", "category": "팔레트", "prices": {
            "무신사": (21200, "https://www.musinsa.com/products/1313594"),
            "에이블리": (18400, "https://m.a-bly.com/goods/2034680"),
            "지그재그": (23000, "https://zigzag.kr/catalog/products/109260628")
        }},
    ]

    keyword = st.text_input("🔍 제품명 검색")
    category = st.selectbox("📂 카테고리", ["전체", "쿠션", "팔레트"])

    filtered = [
        p for p in products
        if (keyword == "" or keyword in p["name"])
        and (category == "전체" or p["category"] == category)
    ]

    if filtered:
        for product in filtered:
            st.markdown(f"""
            <div class="card">
                <h3>🧴 {product['name']}</h3>
            """, unsafe_allow_html=True)

            prices = product["prices"]
            min_price = min([price for price, _ in prices.values() if price > 0])

            for mall, (price, link) in prices.items():
                if price == 0:
                    st.markdown(f"<p>{mall}: 검색 결과 없음</p>", unsafe_allow_html=True)
                elif price == min_price:
                    st.markdown(f"<p>💎 <b>{mall} 최저가: {price}원</b></p>", unsafe_allow_html=True)
                    st.markdown(f'<a href="{link}" target="_blank">구매 링크</a>', unsafe_allow_html=True)
                else:
                    st.markdown(f"<p>{mall}: {price}원</p>", unsafe_allow_html=True)
                    st.markdown(f'<a href="{link}" target="_blank">구매 링크</a>', unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("조건에 맞는 제품이 없습니다.")
