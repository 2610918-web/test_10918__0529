import streamlit as st

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="디지털 자판기", page_icon="🥤", layout="centered")
st.title("🥤 스마트 자판기 앱")
st.write("원하는 음료를 고르고 금액을 투입해 구매해 보세요!")

# 2. 자판기 상품 데이터 (상품명: [가격, 남은수량])
ITEMS = {
    "콜라 🥤": [1500, 5],
    "사이다 🟢": [1200, 3],
    "이온음료 🔹": [1800, 4],
    "캔커피 ☕": [1000, 8],
    "생수 💧": [800, 10]
}

# 3. 세션 상태(Session State) 초기화 - 금액 및 장바구니 유지용
if "balance" not in st.session_state:
    st.session_state.balance = 0
if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- 화면 레이아웃 분할 ---
col1, col2 = st.columns([1.5, 1])

# [왼쪽 영역] 상품 메뉴판
with col1:
    st.subheader("🛒 메뉴판")
    
    for item_name, info in ITEMS.items():
        price, stock = info
        
        # 상품 정보 표시 (가격 및 재고)
        st.markdown(f"**{item_name}** - {price:,}원 (재고: {stock}개)")
        
        # 구매 버튼 (재고가 없을 경우 비활성화)
        if stock > 0:
            if st.button(f"{item_name} 담기", key=item_name):
                # 장바구니에 추가
                if item_name in st.session_state.cart:
                    if st.session_state.cart[item_name] < stock:
                        st.session_state.cart[item_name] += 1
                        st.success(f"{item_name}을(를) 장바구니에 담았습니다.")
                    else:
                        st.error("재고가 부족합니다!")
                else:
                    st.session_state.cart[item_name] = 1
                    st.success(f"{item_name}을(를) 장바구니에 담았습니다.")
        else:
            st.button("품절", key=item_name, disabled=True)
        st.write("---")

# [오른쪽 영역] 금액 투입 및 결제 현황
with col2:
    st.subheader("💰 금액 투입 & 결제")
    
    # 금액 투입 버튼들
    money_input = st.radio("투입할 금액을 선택하세요:", [500, 1000, 5000])
    if st.button("💵 돈 넣기"):
        st.session_state.balance += money_input
        st.toast(f"{money_input:,}원이 투입되었습니다!")

    # 현재 투입된 총 금액 표시
    st.metric(label="현재 투입 금액", value=f"{st.session_state.balance:,} 원")
    
    st.write("---")
    st.subheader("🛒 내 장바구니")
    
    # 장바구니 목록 계산
    total_price = 0
    if st.session_state.cart:
        for cart_item, count in st.session_state.cart.items():
            item_cost = ITEMS[cart_item][0] * count
            total_price += item_cost
            st.write(f"- {cart_item} x {count}개 ({item_cost:,}원)")
        
        st.markdown(f"**총 결제 금액:** {total_price:,}원")
        
        # 결제하기 버튼
        if st.button("💳 결제하기", type="primary"):
            if st.session_state.balance >= total_price:
                # 잔돈 계산 및 장바구니 초기화
                change = st.session_state.balance - total_price
                st.success(f"🎉 결제가 완료되었습니다! 잔돈은 {change:,}원입니다.")
                
                # 구매 완료 후 상태 초기화
                st.session_state.balance = 0
                st.session_state.cart = {}
            else:
                st.error("❌ 투입 금액이 부족합니다! 돈을 더 넣어주세요.")
                
        # 장바구니 비우기 버튼
        if st.button("🗑️ 장바구니 비우기"):
            st.session_state.cart = {}
            st.rerun()
            
    else:
        st.info("장바구니가 비어 있습니다.")
