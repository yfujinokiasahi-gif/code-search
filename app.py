import streamlit as st
import pandas as pd

# ページ設定：中央寄せ
st.set_page_config(page_title="商品検索", layout="centered")

# --- デザインカスタマイズ (CSS) ---
st.markdown("""
    <style>
    /* 1. ヘッダーとメニューを完全に非表示 */
    header[data-testid="stHeader"], #MainMenu, footer {display: none !important;}
    
    /* 2. スマホ画面に100%フィット（横揺れ防止） */
    .block-container {
        width: 100% !important;
        max-width: 100% !important;
        padding: 1.5rem 1rem 1rem 1rem !important;
        overflow-x: hidden !important; 
    }

    /* 3. アプリタイトル */
    .app-title {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #1E293B;
        margin-bottom: 0.5rem !important;
    }

    /* 4. 検索窓とヒット件数の横並び設定（★比率を完全に固定★） */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        width: 100% !important;
        gap: 5px !important;
    }
    
    /* ★修正部分★：検索窓（左側）を画面幅の60%に短く固定 */
    div[data-testid="column"]:nth-of-type(1) { 
        width: 60% !important; 
        flex: 0 0 60% !important; 
        min-width: 0 !important; 
    }
    
    /* ★修正部分★：件数表示（右側）のスペースを40%確保し、絶対に見切れないようにする */
    div[data-testid="column"]:nth-of-type(2) { 
        width: 40% !important; 
        flex: 0 0 40% !important; 
        text-align: right !important;
        white-space: nowrap !important;
        min-width: 0 !important; 
    }

    /* 5. 表の余計な機能（拡大・ダウンロードアイコン）を消す */
    [data-testid="stElementToolbar"] { display: none !important; }

    /* 6. 表全体の幅を画面に合わせる */
    [data-testid="stDataFrame"] { width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# アプリタイトル
st.markdown('<p class="app-title">🔍 商品検索アプリ</p>', unsafe_allow_html=True)

url = "https://docs.google.com/spreadsheets/d/17zsMWCLzo-xUFg_16WGKSEqpFWCLsRCb82EBiml4BiM/export?format=xlsx"

@st.cache_data(ttl="1m")
def get_data():
    return pd.read_excel(url)

# ひらがな・カタカナ変換ロジック
def hira_to_kata(text): return "".join([chr(ord(c) + 96) if "ぁ" <= c <= "ん" else c for c in text])
def kata_to_hira(text): return "".join([chr(ord(c) - 96) if "ァ" <= c <= "ン" else c for c in text])

try:
    df = get_data()
    
    # Python側でも比率を6:4に合わせる
    col1, col2 = st.columns([6, 4]) 
    with col1:
