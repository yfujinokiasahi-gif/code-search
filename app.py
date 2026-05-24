import streamlit as st
import pandas as pd

# ページ設定：centered（中央寄せ）にしてスマホでの集中度を高める
st.set_page_config(page_title="商品検索", layout="centered")

# --- デザインカスタマイズ (CSS) ---
st.markdown("""
    <style>
    /* 1. ヘッダーとメニューを完全に非表示にしてスペースを確保 */
    header[data-testid="stHeader"], #MainMenu, footer {visibility: hidden; display: none !important;}
    
    /* 2. スマホ用メインコンテナの幅と余白調整 */
    .block-container {
        max-width: 500px !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* 3. タイトルを一番上に密着させる */
    .app-title {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #1E293B;
        margin-bottom: 1rem !important;
        text-align: center;
    }

    /* 4. 検索窓とヒット件数を絶対に横並びにする（スマホでも折り返さない） */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
    }
    div[data-testid="column"]:nth-of-type(1) { flex: 4 !important; }
    div[data-testid="column"]:nth-of-type(2) { 
        flex: 1 !important; 
        text-align: right;
        min-width: fit-content;
    }

    /* 5. 表の余計な機能（拡大・ダウンロード）を消す */
    [data-testid="stElementToolbar"] { display: none !important; }

    /* 6. 表のフォントサイズ調整（スマホで見やすく） */
    [data-testid="stTable"] td, [data-testid="stDataFrame"] td {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# アプリタイトル
st.markdown('<p class="app-title">🔍 商品検索アプリ</p>', unsafe_allow_html=True)

url = "https://docs.google.com/spreadsheets/d/17zsMWCLzo-xUFg_16WGKSEqpFWCLsRCb82EBiml4BiM/export?format=xlsx"

@st.cache_data(ttl="1m")
def get_data():
    return pd.read_excel(url)

# 変換ロジック
def hira_to_kata(text): return "".join([chr(ord(c) + 96) if "ぁ" <= c <= "ん" else c for c in text])
def kata_to_hira(text): return "".join([chr(ord(c) - 96) if "ァ" <= c <= "ン" else c for c in text])

try:
    df = get_data()
    st.markdown("##### 品名を入力してください")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("検索", label_visibility="collapsed", placeholder="例：いちご")

    if query:
        qh = kata_to_hira(query); qk = hira_to_kata(query)
        def match(row):
            s = " ".join(map(str, row))
            return (qh in kata_to_hira(s)) or (qk in hira_to_kata(s))
        
        res = df[df.apply(match, axis=1)]
        
        with col2:
            st.markdown(f"**{len(res)}** 件", unsafe_allow_html=True)
        
        if not res.empty:
            # 表示する列を「呼び出しNo.」と「品名（または1列目）」に限定
            # 列名はデータに合わせて自動取得
            cols = res.columns[:2].tolist()
            st.dataframe(res[cols], use_container_width=True, hide_index=True)
        else:
            st.error("見つかりませんでした")
    else:
        st.info("入力を待機中...")

except Exception as e:
    st.error("データの読み込みに失敗しました")
