import streamlit as st
import pandas as pd

# 1. ページの設定（横幅を広く設定）
st.set_page_config(page_title="商品検索アプリ", layout="wide")

# 余白を限界まで削り、スマホでも横並びを強制する設定
st.markdown(
    """
    <style>
    .block-container { padding-top: 0.4rem !important; padding-bottom: 0rem !important; padding-left: 0.8rem !important; padding-right: 0.8rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0.1rem !important; }
    div[data-testid="element-container"] { margin-bottom: 0rem !important; }
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; align-items: center !important; margin-top: -0.4rem !important; }
    div[data-testid="column"]:nth-of-type(1) { flex: 3 1 0% !important; }
    div[data-testid="column"]:nth-of-type(2) { flex: 1.5 1 0% !important; padding-left: 10px !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# タイトル
st.markdown("### **🔍 商品検索アプリ**")

# 正しいスプレッドシートのURL
url = "https://docs.google.com/spreadsheets/d/17zsMWCLzo-xUFg_16WGKSEqpFWCLsRCb82EBiml4BiM/export?format=xlsx"

@st.cache_data(ttl="1m")  # 1分ごとに最新データを読み直す
def get_data():
    return pd.read_excel(url)

# ひらがな ⇔ カタカナの変換関数
def hira_to_kata(text):
    return "".join([chr(ord(c) + 96) if "ぁ" <= c <= "ん" else c for c in text])

def kata_to_hira(text):
    return "".join([chr(ord(c) - 96) if "ァ" <= c <= "ン" else c for c in text])

try:
    df = get_data()
    st.markdown("#### **ここに「品名」を入力**")
    
    col1, col2 = st.columns([3, 1.5])
    with col1:
        query = st.text_input(label="検索窓", label_visibility="collapsed", key="search", placeholder="いちご、すいか、など...")

    if query:
        query_hira = kata_to_hira(query)
        query_kata = hira_to_kata(query)
        
        def match_row(row):
            row_str = " ".join([str(x) for x in row])
            return (query_hira in kata_to_hira(row_str)) or (query_kata in hira_to_kata(row_str))

        mask = df.apply(match_row, axis=1)
        result = df[mask]
        
        if not result.empty:
            with col2:
                st.markdown(f"<p style='color: #2da44e; font-weight: bold; font-size: 15px; margin: 0; white-space: nowrap;'>{len(result)}件</p>", unsafe_allow_html=True)
            
            display_cols = result.columns[:2].tolist()
            
            # 【対策】コピペで絶対に切れないよう、表の表示設定をすべて1行にドッキングしました
            w_config = {display_cols[0]: st.column_config.Column(width=100), display_cols[1]: st.column_config.Column(width=600)}
            st.dataframe(result[display_cols], use_container_width=False, hide_index=True, column_config=w_config)
        else:
            with col2:
                st.markdown("<p style='color: #cf222e; font-weight: bold; font-size: 15px; margin: 0; white-space: nowrap;'>0件</p>", unsafe_allow_html=True)
    else:
        st.info("上の検索窓に品名を入力すると、ここに結果が表示されます。")

except Exception as e:
    st.error(f"データの読み込みに失敗しました。再読み込みしてください。 (詳細: {e})")
