import streamlit as st
import pandas as pd

st.set_page_config(page_title="商品検索アプリ", layout="centered")

# 画面全体のデザイン調整（CSS）
st.markdown(
    """
    <style>
    /* 【修正1】右上の邪魔なアイコン類（Share等）が乗っているヘッダーを完全に消す */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 【修正2】上の余白をギリギリまで削り、タイトルを赤枠の位置に押し上げる */
    .block-container { 
        max-width: 400px !important; 
        padding-top: 1.5rem !important; /* ここの数値で一番上の隙間を調整 */
        padding-bottom: 0rem !important; 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
    }
    
    /* 【修正3】スマホ画面でも絶対に縦並びにさせず、横並び（折り返し禁止）を強制する */
    div[data-testid="stHorizontalBlock"] { 
        flex-wrap: nowrap !important; 
        align-items: center !important; 
    }
    
    /* 検索窓（左）と件数（右）の幅のバランス調整 */
    div[data-testid="column"]:nth-of-type(1) {
        width: 80% !important;
        flex: 1 1 auto !important;
        min-width: 0 !important; /* スマホ画面からはみ出さないように縮小を許可 */
    }
    div[data-testid="column"]:nth-of-type(2) {
        width: 20% !important;
        flex: 0 0 auto !important;
        min-width: 0 !important;
        padding-left: 10px !important; /* 検索窓と件数の間の隙間 */
    }

    /* 表のツールバー（ダウンロードや拡大アイコン）を非表示にする */
    [data-testid="stElementToolbar"] { 
        display: none !important; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

# タイトル（先ほどの赤枠の位置に表示されます）
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
    st.markdown("#### ここに「品名」を入力")
    
    # 検索窓と件数の横幅の割合を設定（4:1の比率）
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(label="検索窓", label_visibility="collapsed", key="search", placeholder="いちご...")

    if query:
        query_hira = kata_to_hira(query)
        query_kata = hira_to_kata(query)
        
        def match_row(row):
            row_str = " ".join([str(x) for x in row])
            return (query_hira in kata_to_hira(row_str)) or (query_kata in hira_to_kata(row_str))

        mask = df.apply(match_row, axis=1)
        result = df[mask]
        
        if not result.empty:
            # 検索窓の右側に件数を表示
            with col2:
                # 検索窓の高さと合わせるために少しだけ上からマージンを取っています
                st.markdown(f"<p style='color: #2da44e; font-weight: bold; font-size: 15px; margin: 5px 0 0 0; white-space: nowrap;'>{len(result)}件</p>", unsafe_allow_html=True)
            
            display_cols = result.columns[:2].tolist()
            
            # 表を表示（スマホの幅にぴったり合わせる）
            st.dataframe(result[display_cols], use_container_width=True, hide_index=True)
        else:
            with col2:
                st.markdown("<p style='color: #cf222e; font-weight: bold; font-size: 15px; margin: 5px 0 0 0; white-space: nowrap;'>0件</p>", unsafe_allow_html=True)
    else:
        st.info("上の検索窓に品名を入力すると、ここに結果が表示されます。")

except Exception as e:
    st.error(f"データの読み込みに失敗しました。再読み込みしてください。 (詳細: {e})")
